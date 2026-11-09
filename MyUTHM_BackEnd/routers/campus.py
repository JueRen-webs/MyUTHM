# routers/campus.py
from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from database import get_db
import crud.campus as crud
from schemas.campus import HostelComplaintCreate, FacilityReservationCreate
from schemas.notification import NotificationCreate

router = APIRouter(prefix="/campus", tags=["Campus Services & Notifications"])

@router.post("/reservations")
def book_facility(reservation: FacilityReservationCreate, db: sqlite3.Connection = Depends(get_db)):
    # 执行同天、同场馆、同时间段防重复冲突预约校验
    result = crud.reserve_facility_reservation = crud.reserve_campus_facility(db, reservation)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.post("/complaints")
def file_complaint(complaint: HostelComplaintCreate, db: sqlite3.Connection = Depends(get_db)):
    success = crud.create_hostel_complaint(db, complaint)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to file hostel complaint")
    return {"message": "Complaint submitted successfully"}

@router.get("/students/{student_id}/complaints")
def list_my_complaints(student_id: str, db: sqlite3.Connection = Depends(get_db)):
    # 前端获取关联转换后的分类名称、跟进老师姓名、状态文本
    return crud.get_student_complaints_list(db, student_id)

@router.post("/notifications")
def create_global_notification(notification: NotificationCreate, db: sqlite3.Connection = Depends(get_db)):
    success = crud.push_global_notification(db, notification)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to create notification")
    return {"message": "Global notification pushed successfully"}

@router.get("/notifications")
def get_recent_notifications(limit: int = 10, db: sqlite3.Connection = Depends(get_db)):
    return crud.fetch_recent_announcements(db, limit)