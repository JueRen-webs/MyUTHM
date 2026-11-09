from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date, time
from decimal import Decimal

class LecturerBase(BaseModel):
    Lecturer_ID: str
    Department_ID: Optional[str] = None
    Position_ID: Optional[str] = None
class LecturerCreate(LecturerBase): pass
class Lecturer(LecturerBase):
    model_config = ConfigDict(from_attributes=True)
class DepartmentBase(BaseModel):
    Department_ID: str
    Department_Name: str
    Department_Email: Optional[EmailStr] = None
    Department_Phone: Optional[str] = None
    Location_ID: Optional[str] = None
class DepartmentCreate(DepartmentBase): pass
class Department(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
class LecturerAttendanceBase(BaseModel):
    Lecturer_Attendance_ID: str
    Lecturer_ID: Optional[str] = None
    Date: Optional[date] = None
    In_Time: Optional[time] = None
    Out_Time: Optional[time] = None
    Details: Optional[str] = None
class LecturerAttendanceCreate(LecturerAttendanceBase): pass
class LecturerAttendance(LecturerAttendanceBase):
    model_config = ConfigDict(from_attributes=True)

class MovementBase(BaseModel):
    Movement_ID: str
    Lecturer_ID: Optional[str] = None
    Start_Date: Optional[date] = None
    End_Date: Optional[date] = None
    Location: Optional[str] = None
    Purpose: Optional[str] = None
class MovementCreate(MovementBase): pass
class Movement(MovementBase):
    model_config = ConfigDict(from_attributes=True)

class MedicalRecordBase(BaseModel):
    Record_ID: str
    Lecturer_ID: Optional[str] = None
    Clinic_ID: Optional[str] = None
    Date: Optional[date] = None
    Charges: Optional[Decimal] = None
class MedicalRecordCreate(MedicalRecordBase): pass
class MedicalRecord(MedicalRecordBase):
    model_config = ConfigDict(from_attributes=True)

class SalaryBase(BaseModel):
    Salary_ID: str
    Lecturer_ID: Optional[str] = None
    Salary_Date: Optional[date] = None
    Basic_Salary: Optional[Decimal] = None
    Bonus: Optional[Decimal] = None
class SalaryCreate(SalaryBase): pass
class Salary(SalaryBase):
    model_config = ConfigDict(from_attributes=True)

class LeavesRecordBase(BaseModel):
    Record_ID: str
    Lecturer_ID: Optional[str] = None
    Leave_Type_ID: Optional[str] = None
    Available_Leave: Optional[int] = None
    Leave_Taken: Optional[int] = None
    Start_Date: Optional[date] = None
    End_Date: Optional[date] = None
    Days: Optional[int] = None
    Note: Optional[str] = None
class LeavesRecordCreate(LeavesRecordBase): pass
class LeavesRecord(LeavesRecordBase):
    model_config = ConfigDict(from_attributes=True)