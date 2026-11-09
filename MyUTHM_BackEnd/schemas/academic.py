from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time, datetime
from decimal import Decimal
class CourseBase(BaseModel):
    Course_ID: str
    Course_Name: str
    Course_Credits: Optional[int] = None
class CourseCreate(CourseBase): pass
class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)

class ProgrammeBase(BaseModel):
    Programme_ID: str
    Programme_Name: str
    Programme_Credits: Optional[int] = None
class ProgrammeCreate(ProgrammeBase): pass
class Programme(ProgrammeBase):
    model_config = ConfigDict(from_attributes=True)

class SectionBase(BaseModel):
    Section_ID: str
    Course_ID: Optional[str] = None
    Lecturer_ID: Optional[str] = None

    Section_Code: Optional[str] = None
    Academic_Session: Optional[str] = None
    Semester: int = None
class SectionCreate(SectionBase): pass
class Section(SectionBase):
    model_config = ConfigDict(from_attributes=True)
class Section_Schedules(BaseModel):
    Section_ID: str
    Class_Type: str
    Day_Of_Week: str
    Start_Time: time
    Start_Time: Optional[time] = None
    End_Time: Optional[time] = None
    Location_ID: Optional[str] = None
class CourseEnrollmentBase(BaseModel):
    Course_Enrollment_ID: str
    Section_ID: Optional[str] = None
    Student_ID: Optional[str] = None
class CourseEnrollmentCreate(CourseEnrollmentBase): pass
class CourseEnrollment(CourseEnrollmentBase):
    model_config = ConfigDict(from_attributes=True)

class CourseAttendanceBase(BaseModel):
    Course_Attendance_ID: str
    Course_Enrollment_ID: Optional[str] = None
    Attendance: Optional[str] = None
    Date: Optional[date] = None
class CourseAttendanceCreate(CourseAttendanceBase): pass
class CourseAttendance(CourseAttendanceBase):
    model_config = ConfigDict(from_attributes=True)

class ResultBase(BaseModel):
    Result_ID: str
    Course_Enrollment_ID: Optional[str] = None
    Final_Grade: Optional[str] = None
    Details: Optional[str] = None
class ResultCreate(ResultBase): pass
class Result(ResultBase):
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time, datetime
from decimal import Decimal

class StreamBase(BaseModel):
    Stream_ID: str
    Lecturer_ID: Optional[str] = None
    Title: Optional[str] = None
    Content: Optional[str] = None
    Created_At: Optional[datetime] = None
class StreamCreate(StreamBase): pass
class Stream(StreamBase):
    model_config = ConfigDict(from_attributes=True)

class LearningMaterialBase(BaseModel):
    Materials_ID: str
    Section_ID: Optional[str] = None
    Title: Optional[str] = None
    Size: Optional[Decimal] = None
    Uploaded_Date: Optional[datetime] = None
    URL: Optional[str] = None
class LearningMaterialCreate(LearningMaterialBase): pass
class LearningMaterial(LearningMaterialBase):
    model_config = ConfigDict(from_attributes=True)

class PastYearQuestionBase(BaseModel):
    Past_Year_ID: str
    Course_ID: Optional[str] = None
    Title: Optional[str] = None
    Size: Optional[Decimal] = None
    URL: Optional[str] = None
class PastYearQuestionCreate(PastYearQuestionBase): pass
class PastYearQuestion(PastYearQuestionBase):
    model_config = ConfigDict(from_attributes=True)

class AssessmentBase(BaseModel):
    Assessment_ID: str
    Section_ID: Optional[str] = None
    Title: Optional[str] = None
    Date: Optional[date] = None
    Start_Time: Optional[time] = None
    End_Time: Optional[time] = None
class AssessmentCreate(AssessmentBase): pass
class Assessment(AssessmentBase):
    model_config = ConfigDict(from_attributes=True)

class AssessmentEnrollmentBase(BaseModel):
    Assessment_Enrollment_ID: str
    Assessment_ID: Optional[str] = None
    Student_ID: Optional[str] = None
    marks: Optional[Decimal] = None
class AssessmentEnrollmentCreate(AssessmentEnrollmentBase): pass
class AssessmentEnrollment(AssessmentEnrollmentBase):
    model_config = ConfigDict(from_attributes=True)

class AssignmentBase(BaseModel):
    Assignment_ID: str
    Section_ID: Optional[str] = None
    Assignment_Type_ID: Optional[str] = None
    Assignment_Title: Optional[str] = None
    Max_Members: Optional[int] = None
    Due_Date: Optional[datetime] = None
class AssignmentCreate(AssignmentBase): pass
class Assignment(AssignmentBase):
    model_config = ConfigDict(from_attributes=True)

class GroupMemberBase(BaseModel):
    Group_ID: str
    Assignment_ID: Optional[str] = None
    Student_ID: str
class GroupMemberCreate(GroupMemberBase): pass
class GroupMember(GroupMemberBase):
    model_config = ConfigDict(from_attributes=True)

class SubmissionBase(BaseModel):
    Submission_ID: str
    Assignment_ID: Optional[str] = None
    Student_ID: Optional[str] = None
    Group_ID: Optional[str] = None
    Submission_Status_ID: Optional[str] = None
    Uploaded_Date: Optional[datetime] = None
class SubmissionCreate(SubmissionBase): pass
class Submission(SubmissionBase):
    model_config = ConfigDict(from_attributes=True)