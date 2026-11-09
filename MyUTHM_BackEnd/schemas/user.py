from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date, time,datetime
from enum import Enum

class RoleEnum(str, Enum):
    Student = 'Student'
    Lecturer = 'Lecturer'
class UserBase(BaseModel):
    User_ID: str
    Name: str
    Email: EmailStr
    Phone: Optional[str] = None
    Role: RoleEnum
    FCM_Token: Optional[str] = None
    Is_Active: bool = True
class UserCreate(UserBase):
    # Create 专有：注册时需要提供密码，但返回 Response 时不会包含
    Password_Hash: str
class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

class LogBase(BaseModel):
    User_ID: Optional[str] = None
    Time: Optional[time] = None
    Date: Optional[date] = None
    Details: Optional[str] = None
class LogCreate(LogBase): pass
class Log(LogBase):
    Log_ID: int
    model_config = ConfigDict(from_attributes=True)
class NotificationBase(BaseModel):
    Notification_ID: str
    Category: Optional[str] = None
    Title: Optional[str] = None
    URL: Optional[str] = None
    Created_Time: Optional[datetime] = None
class NotificationCreate(NotificationBase): pass
class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

class ReminderBase(BaseModel):
    Reminder_ID: str
    User_ID: Optional[str] = None
    Reminder_Status_ID: Optional[str] = None
    Title: Optional[str] = None
    Comment: Optional[str] = None
    Due_Date: Optional[datetime] = None
class ReminderCreate(ReminderBase): pass
class Reminder(ReminderBase):
    model_config = ConfigDict(from_attributes=True)

