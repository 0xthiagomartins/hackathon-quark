from fastapi import APIRouter, status, Response, Request
from src.models import out as omdl
from src.models import inp as imdl
from src.settings import TOKEN_COOKIE_NAME


auth_router = APIRouter()

domain = "/auth"


@auth_router.get("/test", tags=["Health Checker"])
async def test(request: Request):
    return request.client.host


@auth_router.post(
    domain,
    status_code=status.HTTP_201_CREATED,
    tags=["Authorization"],
    response_model=omdl.Tokens,
)
async def login(
    request: Request,
    response: Response,
    credentials: imdl.Credentials,
):
    tokens = request.state.rpc.auth.login(**credentials.model_dump(exclude_unset=True))
    response.set_cookie(
        key=TOKEN_COOKIE_NAME, value=tokens["access_token"], httponly=True
    )
    return tokens


@auth_router.patch(
    domain,
    status_code=status.HTTP_201_CREATED,
    tags=["Authorization"],
    response_model=omdl.Tokens,
)
async def refresh_token(request: Request, response: Response, refresh_token: str):
    tokens = request.state.rpc.auth.refresh_token(refresh_token)
    response.set_cookie(
        key=TOKEN_COOKIE_NAME, value=tokens["access_token"], httponly=True
    )
    return tokens


@auth_router.delete(
    domain,
    tags=["Authorization"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(request: Request):
    request.state.rpc.auth.logout()
