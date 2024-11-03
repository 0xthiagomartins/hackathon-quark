from fastapi import APIRouter, status, Request, File, UploadFile
from src.models import out as omdl
import base64

client_router = APIRouter()
tags = ["Clients Management"]
domain = "/clients"


@client_router.post(
    domain + "/import",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
)
async def import_clients(
    request: Request,
    file: UploadFile = File(...),
):
    content = await file.read()
    b64_data = base64.b64encode(content).decode("utf-8")
    request.state.rpc.importer.import_clients(b64_data)
    return True


@client_router.put(
    domain + "/import",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
)
async def approve_clients(request: Request):
    request.state.rpc.importer.approve_clients()


@client_router.get(
    domain + "/report",
    status_code=status.HTTP_201_CREATED,
    tags=tags,
    response_model=str,
)
async def generate_my_clients_report(request: Request):
    return request.state.rpc.report.my_clients()
