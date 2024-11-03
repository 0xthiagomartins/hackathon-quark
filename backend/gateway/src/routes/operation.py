from fastapi import APIRouter, status, Request, File, UploadFile
from src.models import out as omdl
from src.models import inp as imdl
from src.models import Page
import base64

operation_router = APIRouter()
tags = ["Operation Management"]
domain = "/operations"


@operation_router.post(
    domain + "/import",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
)
async def import_operations(
    request: Request,
    file: UploadFile = File(...),
):
    content = await file.read()
    b64_data = base64.b64encode(content).decode("utf-8")
    request.state.rpc.importer.import_operations(b64_data)
    return True


@operation_router.put(
    domain + "/import",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
)
async def approve_operations(request: Request):
    request.state.rpc.importer.approve_operations()


@operation_router.get(
    domain + "/report/active",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
    response_model=str,
)
async def generate_active_operations_report(request: Request):
    return request.state.rpc.report.active_operations()


@operation_router.get(
    domain + "/report/current",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
    response_model=str,
)
async def generate_current_operations_report(request: Request):
    return request.state.rpc.report.current_operations()
