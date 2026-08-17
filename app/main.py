from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import MedicalStaff
from .schemas import (
    MedicalRegister,
    MedicalLogin,
    TokenResponse,
    PrescriptionCreate
)

from .security import (
    hash_password,
    verify_password,
    create_access_token
)

from .dependencies import (
    get_current_user,
    require_doctor,
    require_medical_staff
)


app = FastAPI(
    title="MedCare E-Prescription API",
    version="1.0.0"
)


Base.metadata.create_all(
    bind=engine
)


@app.get("/")
def root():

    return {
        "message": "MedCare E-Prescription API"
    }

@app.post("/api/v1/medical/register")
def register_medical_staff(
    data: MedicalRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(MedicalStaff)
        .filter(
            MedicalStaff.username == data.username
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại"
        )

    hashed_password = hash_password(
        data.password
    )

    staff = MedicalStaff(
        username=data.username,
        hashed_password=hashed_password,
        role=data.role
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return {
        "message": "Đăng ký thành công",
        "username": staff.username,
        "role": staff.role
    }

@app.post(
    "/api/v1/medical/login",
    response_model=TokenResponse
)
def medical_login(
    data: MedicalLogin,
    db: Session = Depends(get_db)
):

    staff = (
        db.query(MedicalStaff)
        .filter(
            MedicalStaff.username == data.username
        )
        .first()
    )

    if not staff:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác"
        )

    password_valid = verify_password(
        data.password,
        staff.hashed_password
    )

    if not password_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác"
        )

    access_token = create_access_token(
        username=staff.username,
        role=staff.role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/api/v1/prescriptions")
def create_prescription(
    prescription: PrescriptionCreate,
    current_user: dict = Depends(
        require_doctor
    )
):

    return {
        "message": "Tạo đơn thuốc thành công",

        "doctor": current_user["username"],

        "prescription": {
            "patient_name": prescription.patient_name,
            "medicine": prescription.medicine,
            "dosage": prescription.dosage,
            "quantity": prescription.quantity
        }
    }

@app.get("/api/v1/prescriptions/view")
def view_prescriptions(
    current_user: dict = Depends(
        require_medical_staff
    )
):

    return {
        "message": "Được phép xem đơn thuốc",

        "user": current_user["username"],

        "role": current_user["role"],

        "prescriptions": [
            {
                "id": 1,
                "patient_name": "Nguyen Van A",
                "medicine": "Paracetamol",
                "dosage": "500mg",
                "quantity": 10
            },
            {
                "id": 2,
                "patient_name": "Tran Thi B",
                "medicine": "Amoxicillin",
                "dosage": "500mg",
                "quantity": 15
            }
        ]
    }