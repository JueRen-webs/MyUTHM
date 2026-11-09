# routers/lecturers.py
from fastapi import APIRouter, Depends, HTTPException
import sqlite3
from database import get_db
import crud.lecturer as crud
from schemas.lecturer import LecturerAttendanceCreate, LeavesRecordCreate

router = APIRouter(prefix="/lecturers", tags=["Lecturer HR & Attendance"])

@router.get("/{lecturer_id}/profile")
def get_lecturer_profile(lecturer_id: str, db: sqlite3.Connection = Depends(get_db)):
    profile = crud.get_lecturer_profile(db, lecturer_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Lecturer profile not found")
    return profile

@router.post("/attendance/clock")
def clock_in_out(attendance: LecturerAttendanceCreate, db: sqlite3.Connection = Depends(get_db)):
    # 自动识别是今日首次打卡(Clock-In)还是重复打卡签退(Clock-Out)
    return crud.clock_in_out_lecturer(db, attendance)

@router.post("/leave/apply")
def apply_leave(leave: LeavesRecordCreate, requested_days: int, db: sqlite3.Connection = Depends(get_db)):
    # 执行带 Available_Leave 扣减与余假不足拦截的人事逻辑
    result = crud.apply_lecturer_leave(db, leave, requested_days)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result