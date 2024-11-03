from fastapi import APIRouter, status, Request
from src.models import out as omdl
from src.models import inp as imdl
from src.models import Page

user_router = APIRouter()
tags = ["User"]
domain = "/users"


@user_router.post(
    domain + "/{role_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["User Management"],
    response_model=int,
)
async def register_user(request: Request, role_id: int, user_form: imdl.UserForm):
    print("123" * 25)
    user_id = request.state.rpc.auth.register_user(
        role_id, **user_form.model_dump(exclude_unset=True)
    )
    print("123" * 25)
    return user_id
