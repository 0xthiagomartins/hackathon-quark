import logging
from fastapi.middleware.cors import CORSMiddleware
from .utils import treat_return_exception, authorize, is_blocked
from nameko.standalone.rpc import ClusterRpcProxy
from fastapi import Request
from werkzeug.exceptions import Unauthorized
from . import create_app

app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("https")
@app.middleware("http")
async def treat_request(request: Request, call_next):
    call_endpoint = False
    access_token = None
    try:
        logging.info(f"Starting request: [{request.url.path}]")
        if not any(
            [
                (
                    request.url.path.endswith("/auth")
                    and request.method in ["POST", "PUT"]
                ),
                "test" in request.url.path,
                "/auth/user" in request.url.path,
                "/auth" in request.url.path and request.method != "DELETE",
                request.url.path.endswith("/user") and request.method == "POST",
                request.url.path.endswith("/docs"),
                request.url.path.endswith("/redoc"),
                request.url.path.endswith("/openapi.json"),
            ]
        ):
            access_token = authorize(request)
        with ClusterRpcProxy() as rpc:
            if access_token:
                (
                    tokens,
                    user_id,
                    roles,
                ) = rpc.auth.validate_token(access_token)
                if is_blocked(roles, request):
                    raise Unauthorized("Unauthorized request")
                request.state.context_data = {
                    "tokens": tokens,
                    "user_id": user_id,
                    "roles": roles,
                }
                rpc.context_data["session_data"] = {
                    "user_id": user_id,
                    "roles": roles,
                }
            request.state.rpc = rpc
            call_endpoint = True
            response = await call_next(request)
        return response
    except Exception as err:
        return treat_return_exception(err, call_endpoint)
