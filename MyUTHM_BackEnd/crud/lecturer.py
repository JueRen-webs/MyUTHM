import sqlite3
from schemas.lecturer import LecturerAttendanceCreate, LeavesRecordCreate

# 核心 JOIN 查询：获取讲师档案，拼出职称和部门名
def get_lecturer_profile(db: sqlite3.Connection, lecturer_id: str) -> dict | None:
    cursor = db.cursor()
    query = """
        SELECT u.User_ID, u.Name, u.Email, u.Phone,
               d.Department_Name, p.Position_Name
        FROM Users u
        JOIN Lecturers l ON u.User_ID = l.Lecturer_ID
        LEFT JOIN Departments d ON l.Department_ID = d.Department_ID
        LEFT JOIN Positions p ON l.Position_ID = p.Position_ID
        WHERE u.User_ID = ?
    """
    cursor.execute(query, (lecturer_id,))
    row = cursor.fetchone()
    return dict(row) if row else None
def get_all_departments_with_location(db: sqlite3.Connection) -> list[dict]:
    cursor = db.cursor()
    query = """
        SELECT d.Department_ID, d.Department_Name, d.Department_Email, d.Department_Phone,
               l.Location_Name, l.Location_URL
        FROM Departments d
        LEFT JOIN Locations l ON d.Location_ID = l.Location_ID
    """
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]
# 核心商业逻辑：打卡考勤（支持每日首次打卡 INSERT，下班重复打卡 UPDATE 的智能识别）
def clock_in_out_lecturer(db: sqlite3.Connection, att: LecturerAttendanceCreate) -> dict:
    cursor = db.cursor()
    att_date = att.Date.strftime("%Y-%m-%d") if att.Date else None

    # 检查今天这个老师有没有打过卡
    cursor.execute(
        "SELECT * FROM Lecturer_Attendance WHERE Lecturer_ID = ? AND Date = ?",
        (att.Lecturer_ID, att_date)
    )
    existing_record = cursor.fetchone()

    in_time_str = att.In_Time.strftime("%H:%M:%S") if att.In_Time else None
    out_time_str = att.Out_Time.strftime("%H:%M:%S") if att.Out_Time else None

    if not existing_record:
        # 今天第一次打卡：上班签到
        cursor.execute(
            """
            INSERT INTO Lecturer_Attendance (Lecturer_Attendance_ID, Lecturer_ID, Date, In_Time, Out_Time, Details)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (att.Lecturer_Attendance_ID, att.Lecturer_ID, att_date, in_time_str, out_time_str, att.Details)
        )
        db.commit()
        return {"status": "Clock-In Recorded"}
    else:
        # 今天有打卡记录：属于下班签退，自动执行 UPDATE 补全 Out_Time
        cursor.execute(
            """
            UPDATE Lecturer_Attendance 
            SET Out_Time = ?, Details = ? 
            WHERE Lecturer_ID = ? AND Date = ?
            """,
            (out_time_str if out_time_str else "17:00:00", att.Details, att.Lecturer_ID, att_date)
        )
        db.commit()
        return {"status": "Clock-Out Updated"}

# 核心商业逻辑：讲师请假审批扣减系统
def apply_lecturer_leave(db: sqlite3.Connection, leave: LeavesRecordCreate, requested_days: int) -> dict:
    cursor = db.cursor()

    # 1. 查询该讲师该假别（如年假/病假）目前最新的一条记录，算出剩余天数
    cursor.execute(
        """
        SELECT Available_Leave, Leave_Taken FROM Leaves_Records 
        WHERE Lecturer_ID = ? AND Leave_Type_ID = ? 
        ORDER BY Record_ID DESC LIMIT 1
        """,
        (leave.Lecturer_ID, leave.Leave_Type_ID)
    )
    last_record = cursor.fetchone()

    current_available = last_record["Available_Leave"] if last_record else 30 # 默认年假包30天
    current_taken = last_record["Leave_Taken"] if last_record else 0

    # 2. 扣减检查拦截
    if current_available < requested_days:
        return {"success": False, "message": "Application rejected: Insufficient leave balance!"}

    # 3. 重新计算最新指标并写入新记录
    new_available = current_available - requested_days
    new_taken = current_taken + requested_days

    cursor.execute(
        """
        INSERT INTO Leaves_Records (Record_ID, Lecturer_ID, Leave_Type_ID, Available_Leave, Leave_Taken)
        VALUES (?, ?, ?, ?, ?)
        """,
        (leave.Record_ID, leave.Lecturer_ID, leave.Leave_Type_ID, new_available, new_taken)
    )
    db.commit()
    return {"success": True, "message": "Leave approved", "remaining_balance": new_available}