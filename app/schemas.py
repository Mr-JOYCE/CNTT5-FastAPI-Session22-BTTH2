from typing import Literal

from pydantic import BaseModel, Field


class MedicalRegister(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )

    role: Literal["doctor", "pharmacist"]


class MedicalLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PrescriptionCreate(BaseModel):
    patient_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    medicine: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    dosage: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    quantity: int = Field(
        ...,
        gt=0
    )