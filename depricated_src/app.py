
# here is app.py

from indented_logger import setup_logging
import logging
from fastapi import Depends, Request

import os

log_file_path = os.path.expanduser("~/my_logs/app.log")
# log_file_path = "/var/log/my_app/app.log"

log_dir = os.path.dirname(log_file_path)
os.makedirs(log_dir, exist_ok=True)


setup_logging(level=logging.DEBUG,
            log_file=log_file_path, 
            include_func=True, 
            include_module=False, 
            no_datetime=True, 
            min_func_name_col=100 )


logging.getLogger("passlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

logger.debug("start")
import logging


from fastapi import FastAPI
from core.dependencies import setup_dependencies

from apis.tasks_api import router as TaskApiRouter
from apis.wallet_api import router as WalletApiRouter
from apis.auth_api import router as AuthApiRouter


from starlette.middleware.base import BaseHTTPMiddleware
import uuid


import logging
# from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="crowbay API",
    description="API for processing crowbay requests",
    version="1.0.0",
)


origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:5174",

    
    "https://budgety-ui-70638306280.europe-west1.run.app",
    "https://dev-budgety-ui-70638306280.us-central1.run.app" , 

    
    "https://budgety.ai" ,
    "https://www.budgety.ai"

]


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a new UUID for this request
        request_id = str(uuid.uuid4())
        
        # Optionally, add the request_id to headers for downstream usage
        # (e.g., logging or returning to the client)
        request.state.request_id = request_id

        # You can also add it as a header in the response
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins , # Adjust this to more specific domains for security
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.add_middleware(RequestIDMiddleware)



app.include_router(TaskApiRouter)
app.include_router(WalletApiRouter)
app.include_router(AuthApiRouter)


services = setup_dependencies()

@app.on_event("startup")
async def startup_event():
    app.state.services = services
    logger.debug("Configurations loaded and services initialized")





