from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class VehicleBase(BaseModel):
    User_ID: Optional[str] = None
    Vehicle_Type_ID: Optional[str] = None
    Plate_Number: str
    Model: Optional[str] = None
    Color: Optional[str] = None
    Registration_Date: Optional[date] = None
    Session_Year: Optional[str] = None
class VehicleCreate(VehicleBase): pass
class Vehicle(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

class FacilityReservationBase(BaseModel):
    Reservation_ID: str
    User_ID: Optional[str] = None
    Facility_ID: Optional[str] = None
    Date: Optional[date] = None
    TimeSlot: Optional[str] = None
class FacilityReservationCreate(FacilityReservationBase): pass
class FacilityReservation(FacilityReservationBase):
    model_config = ConfigDict(from_attributes=True)

class HostelRegistrationBase(BaseModel):
    Reg_ID: str
    Student_ID: Optional[str] = None
    Hostel_ID: Optional[str] = None
    Check_In_Date: Optional[date] = None
    Check_Out_Date: Optional[date] = None
class HostelRegistrationCreate(HostelRegistrationBase): pass
class HostelRegistration(HostelRegistrationBase):
    model_config = ConfigDict(from_attributes=True)

class ElectricalStickerBase(BaseModel):
    Electrical_Sticker_ID: str
    Student_ID: Optional[str] = None
    Appliance_ID: Optional[str] = None
    Number_Of_Appliance: Optional[int] = None
    Expiry_Date: Optional[date] = None
class ElectricalStickerCreate(ElectricalStickerBase): pass
class ElectricalSticker(ElectricalStickerBase):
    model_config = ConfigDict(from_attributes=True)

class HostelComplaintBase(BaseModel):
    Complaint_ID: str
    Student_ID: Optional[str] = None
    Complaint_Category_ID: Optional[str] = None
    Complaint_Status_ID: Optional[str] = None
    Handled_By_Lecturer_ID: Optional[str] = None
    Description: Optional[str] = None
class HostelComplaintCreate(HostelComplaintBase): pass
class HostelComplaint(HostelComplaintBase):
    model_config = ConfigDict(from_attributes=True)