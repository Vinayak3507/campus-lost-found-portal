from fastapi import (APIRouter,Depends,HTTPException,status,)
from app.dependencies.auth import get_current_user
from app.schema.report_schema import (ReportCreateRequest,ReportCreateResponse,)
from app.services.report_services import ReportService

router = APIRouter(tags=["Reports"],)

@router.post("/reports",response_model=ReportCreateResponse,status_code=status.HTTP_201_CREATED,)
def create_report_endpoint(report: ReportCreateRequest,current_user: dict = Depends(get_current_user),):

    try:
        return ReportService.create_new_report(current_user["id"],report,)

    except ValueError as e:
        if str(e) == "You have already submitted a similar active report.":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e),)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e),)