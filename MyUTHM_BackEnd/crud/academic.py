import sqlite3
from schemas.academic import AssignmentCreate, SubmissionCreate

# 核心 JOIN 查询：全校综合课表。Flutter 端不能只显示一堆 ID，必须全部转换为人类可读的名称
def get_comprehensive_timetable(db: sqlite3.Connection) -> list[dict]:
    cursor = db.cursor()
    query = """
        SELECT s.Section_ID, s.Section_Code, s.Start_Time, s.End_Time, s.Session_Year,
               c.Course_Name, c.Course_Credits,
               u.Name as Lecturer_Name,
               l.Location_Name, l.Location_URL
        FROM Sections s
        JOIN Courses c ON s.Course_ID = c.Course_ID
        JOIN Lecturers lec ON s.Lecturer_ID = lec.Lecturer_ID
        JOIN Users u ON lec.Lecturer_ID = u.User_ID
        LEFT JOIN Locations l ON s.Location_ID = l.Location_ID
    """
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]

# 核心商业逻辑：学生在线选课流程（防止超卖/人数爆满验证）
def enroll_student_into_section(db: sqlite3.Connection, student_id: str, section_id: str) -> dict:
    cursor = db.cursor()

    # 1. 业务步骤一：查验该课程允许的最大人数上限 (Max_Number_Students)
    cursor.execute(
        """
        SELECT c.Max_Number_Students, c.Course_Name 
        FROM Sections s
        JOIN Courses c ON s.Course_ID = c.Course_ID
        WHERE s.Section_ID = ?
        """, (section_id,)
    )
    course_info = cursor.fetchone()
    if not course_info:
        return {"success": False, "message": "The selected course section does not exist"}

    max_capacity = course_info["Max_Number_Students"]

    # 2. 业务步骤二：查询该班级目前已经有多少人报了名
    cursor.execute(
        "SELECT COUNT(*) as enrolled_count FROM Courses_Enrollments WHERE Section_ID = ?",
        (section_id,)
    )
    current_count = cursor.fetchone()["enrolled_count"]

    # 3. 业务步骤三：高并发抢课名额拦截
    if max_capacity is not None and current_count >= max_capacity:
        return {
            "success": False,
            "message": f"Enrollment failed! [{course_info['Course_Name']}] has reached its limit of {max_capacity} students."
        }

    # 4. 验证通过，允许写入多对多 Join Table
    import uuid
    enrollment_id = str(uuid.uuid4())[:8]
    cursor.execute(
        "INSERT INTO Courses_Enrollments (Course_Enrollment_ID, Section_ID, Student_ID) VALUES (?, ?, ?)",
        (enrollment_id, section_id, student_id)
    )
    db.commit()
    return {"success": True, "message": "Enrolled successfully", "enrollment_id": enrollment_id}

# ==================== 作业与提交处理 ====================

def create_new_assignment(db: sqlite3.Connection, asm: AssignmentCreate) -> bool:
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO Assignments (Assignment_ID, Section_ID, Assignment_Type_ID, Assignment_Title, Max_Members, Due_Date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (asm.Assignment_ID, asm.Section_ID, asm.Assignment_Type_ID, asm.Assignment_Title,
         asm.Max_Members, asm.Due_Date.strftime("%Y-%m-%d %H:%M:%S") if asm.Due_Date else None)
    )
    db.commit()
    return True

def submit_student_assignment(db: sqlite3.Connection, sub: SubmissionCreate) -> bool:
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO Submissions (Submission_ID, Assignment_ID, Student_ID, Group_ID, Submission_Status_ID, Uploaded_Date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (sub.Submission_ID, sub.Assignment_ID, sub.Student_ID, sub.Group_ID, sub.Submission_Status_ID,
         sub.Uploaded_Date.strftime("%Y-%m-%d %H:%M:%S") if sub.Uploaded_Date else None)
    )
    db.commit()
    return True