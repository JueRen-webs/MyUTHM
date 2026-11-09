# routers/academic.py
from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from database import get_db
import crud.academic as crud
from schemas.academic import AssignmentCreate, SubmissionCreate

router = APIRouter(prefix="/academic", tags=["Academic & Coursework"])

@router.get("/timetable")
def get_timetable(db: sqlite3.Connection = Depends(get_db)):
    # 获取全校人类可读的综合课表（已JOIN关联讲师名、教室名和课程名）
    return crud.get_comprehensive_timetable(db)

@router.post("/sections/{section_id}/enroll")
def enroll_course_section(section_id: str, student_id: str, db: sqlite3.Connection = Depends(get_db)):
    # 执行包含 Max_Number_Students 名额防超卖校验的抢课系统
    result = crud.enroll_student_into_section(db, student_id, section_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result

@router.post("/assignments")
def publish_assignment(assignment: AssignmentCreate, db: sqlite3.Connection = Depends(get_db)):
    success = crud.create_new_assignment(db, assignment)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to publish assignment")
    return {"message": "Assignment published successfully"}

@router.post("/submissions")
def submit_assignment(submission: SubmissionCreate, db: sqlite3.Connection = Depends(get_db)):
    success = crud.submit_student_assignment(db, submission)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to submit assignment")
    return {"message": "Assignment submitted successfully"}