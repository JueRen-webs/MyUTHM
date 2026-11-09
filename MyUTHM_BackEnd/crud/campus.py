# crud/campus.py
import sqlite3
from schemas.campus import HostelComplaintCreate, FacilityReservationCreate, VehicleCreate
from schemas.notification import NotificationCreate

def get_vehicle_by_plate(db: sqlite3.Connection, plate_number: str):
    """根据车牌号查询车辆（用于查重和最后的数据返回）"""
    cursor = db.cursor()
    # 强制大写比对
    cursor.execute("SELECT * FROM Vehicles WHERE UPPER(Plate_Number) = ?;", (plate_number.upper(),))
    return cursor.fetchone()

def register_new_vehicle(db: sqlite3.Connection, vehicle: VehicleCreate):
    """
    业务逻辑：为学生或教职工引进/登记一辆新车 (Vehicle_ID 已改为自动递增)
    """
    # 1. 强校验：检查车牌号是否已经被注册过了
    existing_plate = get_vehicle_by_plate(db, vehicle.Plate_Number)
    if existing_plate:
        return {"success": False, "message": f"Plate number '{vehicle.Plate_Number}' is already registered."}

    # 2. 准备写入数据库（💡 去掉了 SQL 语句和参数中的 Vehicle_ID）
    cursor = db.cursor()
    sql = """
        INSERT INTO Vehicles (
            User_ID, Vehicle_Type_ID, Plate_Number, 
            Model, Color, Registration_Date, Session_Year
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """

    # SQLite 不支持原生的 date 类型，需要将其转为字符串 (YYYY-MM-DD)
    reg_date_str = vehicle.Registration_Date.isoformat() if vehicle.Registration_Date else None

    try:
        cursor.execute(sql, (
            vehicle.User_ID,
            vehicle.Vehicle_Type_ID,
            vehicle.Plate_Number,
            vehicle.Model,
            vehicle.Color,
            reg_date_str,
            vehicle.Session_Year
        ))
        db.commit()

        # 3. 通过独一无二的车牌号重新查出刚插入的数据（此时已包含 SQLite 自动生成的整型 Vehicle_ID）
        return {
            "success": True,
            "message": "Vehicle registered successfully",
            "data": get_vehicle_by_plate(db, vehicle.Plate_Number)
        }
    except sqlite3.IntegrityError as e:
        db.rollback()
        return {"success": False, "message": f"Database integrity error: {str(e)}. Please check foreign keys."}

# ==================== 核心商业逻辑：后勤场馆/设施预订 ====================
def reserve_campus_facility(db: sqlite3.Connection, res: FacilityReservationCreate) -> dict:
    cursor = db.cursor()
    res_date = res.Date.strftime("%Y-%m-%d") if res.Date else None

    # 检查该场馆在当天的该时段是否已经被捷足先登
    cursor.execute(
        """
        SELECT COUNT(*) as booked_count FROM Facility_Reservations 
        WHERE Facility_ID = ? AND Date = ? AND TimeSlot = ?
        """,
        (res.Facility_ID, res_date, res.TimeSlot)
    )
    if cursor.fetchone()["booked_count"] > 0:
        return {"success": False, "message": "Conflict! This slot has already been reserved by another user."}

    # 预约写入
    cursor.execute(
        """
        INSERT INTO Facility_Reservations (Reservation_ID, User_ID, Facility_ID, Date, TimeSlot)
        VALUES (?, ?, ?, ?, ?)
        """,
        (res.Reservation_ID, res.User_ID, res.Facility_ID, res_date, res.TimeSlot)
    )
    db.commit()
    return {"success": True, "message": "Facility reserved successfully", "id": res.Reservation_ID}

# ==================== 宿舍报修与投诉处理 ====================
def create_hostel_complaint(db: sqlite3.Connection, comp: HostelComplaintCreate) -> bool:
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO Hostel_Complaints (Complaint_ID, Student_ID, Complaint_Category_ID, Complaint_Status_ID, Handled_By_Lecturer_ID, Description)
        VALUES (?, ?, ?, ?, NULL, ?)
        """,
        (comp.Complaint_ID, comp.Student_ID, comp.Complaint_Category_ID, comp.Complaint_Status_ID, comp.Description)
    )
    db.commit()
    return True

# 核心 JOIN 查询：学生查看自己的报修单进度，需要带出状态文字、大类名字和跟进老师名字
def get_student_complaints_list(db: sqlite3.Connection, student_id: str) -> list[dict]:
    cursor = db.cursor()
    query = """
        SELECT hc.Complaint_ID, hc.Description,
               cc.Category as Category_Name,
               cs.Complaint_Status as Status_Text,
               u.Name as Handler_Teacher_Name
        FROM Hostel_Complaints hc
        LEFT JOIN Complaints_Categories cc ON hc.Complaint_Category_ID = cc.Complaint_Category_ID
        LEFT JOIN Complaint_Statuses cs ON hc.Complaint_Status_ID = cs.Complaint_Status_ID
        LEFT JOIN Users u ON hc.Handled_By_Lecturer_ID = u.User_ID
        WHERE hc.Student_ID = ?
    """
    cursor.execute(query, (student_id,))
    return [dict(row) for row in cursor.fetchall()]

# ==================== 通知系统 ====================
def push_global_notification(db: sqlite3.Connection, notif: NotificationCreate) -> bool:
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO Notifications (Notification_ID, Category, Title, URL)
        VALUES (?, ?, ?, ?)
        """,
        (notif.Notification_ID, notif.Category, notif.Title, notif.URL)
    )
    db.commit()
    return True

def fetch_recent_announcements(db: sqlite3.Connection, limit: int = 10) -> list[dict]:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Notifications ORDER BY Created_Time DESC LIMIT ?", (limit,))
    return [dict(row) for row in cursor.fetchall()]