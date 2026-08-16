from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.enums import (ReportTypeEnum,VisibilityEnum,ImportanceEnum,ReportStatusEnum,)

class ReportCreateRequest(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True)
    report_type: ReportTypeEnum
    category_id: str
    title: str = Field(...,min_length=3,max_length=150,)
    description: str | None = Field(default=None,max_length=2000,)
    location: str | None = Field(default=None,max_length=255,)
    date_time: datetime | None = None
    image_url: str | None = Field(default=None,max_length=255,)
    visibility: VisibilityEnum = VisibilityEnum.PUBLIC
    importance: ImportanceEnum = ImportanceEnum.MEDIUM

class ReportResponse(BaseModel):

    id: str
    user_id: str
    report_type: ReportTypeEnum
    category_id: str | None = None
    title: str
    description: str | None = None
    location: str | None = None
    date_time: datetime | None = None
    image_url: str | None = None
    status: ReportStatusEnum
    visibility: VisibilityEnum
    importance: ImportanceEnum
    created_at: datetime
    updated_at: datetime

class ReportCreateResponse(BaseModel):
    message: str
    report_id: str