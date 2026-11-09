# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from database import get_db
import crud.users as crud
from pydantic import BaseModel
# 💡 如果你的 schema 文件在 schemas 文件夹下，请改为 from schemas.user import ...
from schemas.user import UserCreate, User, LogCreate

router = APIRouter(prefix="/users", tags=["Users & System"])
class LoginRequest(BaseModel):
    user_id: str
    password_hash: str
# 👇 这里已修正为标准的 HTTP_201_CREATED
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):

    # 2. 校验 ID 是否已被占用
    existing_id = crud.get_user_by_id(db, user.User_ID)
    if existing_id:
        raise HTTPException(status_code=400, detail="User ID already exists")

    return crud.create_user(db, user)

@router.post("/login")
def login_user(request: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    # 从 request 里拿出数据
    user = crud.get_user_by_id(db, request.user_id)

    if not user or user["Password_Hash"] != request.password_hash:
        raise HTTPException(status_code=401, detail="Invalid User ID or Password")
    if not user["Is_Active"]:
        raise HTTPException(status_code=403, detail="User account is deactivated")

    return {"message": "Login successful", "role": user["Role"], "user_id": user["User_ID"]}

@router.get("/departments/locations")
def list_departments(db: sqlite3.Connection = Depends(get_db)):
    return crud.get_all_departments_with_location(db)

@router.post("/logs")
def create_log(log: LogCreate, db: sqlite3.Connection = Depends(get_db)):
    success = crud.write_system_log(db, log)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to write system log")
    return {"message": "Log recorded successfully"}