# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

import logging
logger = logging.getLogger(__name__)
logging.getLogger("multipart").setLevel(logging.WARNING)
logging.getLogger("multipart.multipart").setLevel(logging.WARNING)


import impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from models.extra_models import TokenModel  # noqa: F401
from datetime import datetime
from pydantic import Field, StrictBytes, StrictFloat, StrictInt, StrictStr, field_validator
from typing import List, Optional, Tuple, Union
from typing_extensions import Annotated
from models.accept_task200_response import AcceptTask200Response
from models.accept_task404_response import AcceptTask404Response
from models.add_balance400_response import AddBalance400Response
from models.add_balance401_response import AddBalance401Response
from models.add_balance500_response import AddBalance500Response
from models.create_task201_response import CreateTask201Response
from models.create_task_request import CreateTaskRequest
from models.list_my_tasks200_response_inner import ListMyTasks200ResponseInner
from models.list_participated_tasks200_response_inner import ListParticipatedTasks200ResponseInner
from models.list_tasks200_response_inner import ListTasks200ResponseInner
from models.open_dispute200_response import OpenDispute200Response
from models.open_dispute404_response import OpenDispute404Response
from models.open_dispute_request import OpenDisputeRequest
from models.reject_task_after_acceptance200_response import RejectTaskAfterAcceptance200Response
from models.reject_task_after_acceptance404_response import RejectTaskAfterAcceptance404Response
from models.task_validation200_response import TaskValidation200Response
from models.validate_task_finished200_response import ValidateTaskFinished200Response
from models.validate_task_finished_request import ValidateTaskFinishedRequest
from security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)



from typing import Optional, Annotated
from pydantic import Field, StrictStr
from fastapi import Depends, Request

def get_request_handler():
    from app import app
    from impl.request_handler import RequestHandler
    return RequestHandler(app)

def get_request_id(request: Request):
    # Retrieve the request_id from request.state
    return request.state.request_id


@router.post(
    "/tasks/{taskId}/accept",
    responses={
        200: {"model": AcceptTask200Response, "description": "Task accepted successfully"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        404: {"model": AcceptTask404Response, "description": "Task not found"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="Accept a task",
    response_model_by_alias=True,
)
async def accept_task(
    taskId: Annotated[StrictStr, Field(description="The ID of the task to accept")] = Path(..., description="The ID of the task to accept"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AcceptTask200Response:
    """Allows a user to accept a task, indicating they will complete it."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().accept_task(taskId)


@router.post(
    "/tasks",
    responses={
        201: {"model": CreateTask201Response, "description": "Task created successfully"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="Create a new task",
    response_model_by_alias=True,
)
async def create_task(
    create_task_request: CreateTaskRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> CreateTask201Response:
    """Allows a user to create a task with specified budget, filters, deadlines, etc."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().create_task(create_task_request)


@router.get(
    "/tasks/my",
    responses={
        200: {"model": List[ListMyTasks200ResponseInner], "description": "A list of tasks created by the user"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="List tasks created by the authenticated user",
    response_model_by_alias=True,
)
async def list_my_tasks(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[ListMyTasks200ResponseInner]:
    """Returns all tasks that the user has created."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().list_my_tasks()


@router.get(
    "/tasks/participated",
    responses={
        200: {"model": List[ListParticipatedTasks200ResponseInner], "description": "A list of tasks the user participated in"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="List tasks the user has participated in",
    response_model_by_alias=True,
)
async def list_participated_tasks(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[ListParticipatedTasks200ResponseInner]:
    """Returns tasks that the user accepted or performed in the past or is currently performing."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().list_participated_tasks()


@router.get(
    "/tasks",
    responses={
        200: {"model": List[ListTasks200ResponseInner], "description": "A list of tasks"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="List tasks",
    response_model_by_alias=True,
)
async def list_tasks(
    user_attribute_filters: Annotated[Optional[StrictStr], Field(description="Custom user-attribute filters (format can vary)")] = Query(None, description="Custom user-attribute filters (format can vary)", alias="user_attribute_filters"),
    total_budget: Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="Filter tasks by total budget (e.g. >= this value)")] = Query(None, description="Filter tasks by total budget (e.g. &gt;&#x3D; this value)", alias="total_budget"),
    you_earn: Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="Filter tasks by how much a doer can earn")] = Query(None, description="Filter tasks by how much a doer can earn", alias="you_earn"),
    status: Annotated[Optional[StrictStr], Field(description="Filter tasks by status")] = Query(None, description="Filter tasks by status", alias="status"),
    creation_date: Annotated[Optional[datetime], Field(description="Filter tasks created on or after this date")] = Query(None, description="Filter tasks created on or after this date", alias="creation_date"),
    partition_deadline: Annotated[Optional[datetime], Field(description="Filter tasks with a partition deadline on or after this date")] = Query(None, description="Filter tasks with a partition deadline on or after this date", alias="partition_deadline"),
    submission_deadline: Annotated[Optional[datetime], Field(description="Filter tasks with a submission deadline on or after this date")] = Query(None, description="Filter tasks with a submission deadline on or after this date", alias="submission_deadline"),
    category: Annotated[Optional[StrictStr], Field(description="Filter tasks by category (e.g., \"social_media\", \"marketing\")")] = Query(None, description="Filter tasks by category (e.g., \&quot;social_media\&quot;, \&quot;marketing\&quot;)", alias="category"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[ListTasks200ResponseInner]:
    """Retrieve a list of tasks with optional filtering."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().list_tasks(user_attribute_filters, total_budget, you_earn, status, creation_date, partition_deadline, submission_deadline, category)


@router.post(
    "/tasks/{taskId}/dispute",
    responses={
        200: {"model": OpenDispute200Response, "description": "Dispute opened successfully"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        404: {"model": OpenDispute404Response, "description": "Task not found"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="Open a dispute on a task",
    response_model_by_alias=True,
)
async def open_dispute(
    taskId: Annotated[StrictStr, Field(description="The ID of the task to dispute")] = Path(..., description="The ID of the task to dispute"),
    open_dispute_request: OpenDisputeRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> OpenDispute200Response:
    """Allows either the task creator or task doer to open a dispute if there’s disagreement about task completion, payment, etc."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().open_dispute(taskId, open_dispute_request)


@router.post(
    "/tasks/{taskId}/reject",
    responses={
        200: {"model": RejectTaskAfterAcceptance200Response, "description": "Task rejected successfully"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        404: {"model": RejectTaskAfterAcceptance404Response, "description": "Task not found or cannot be rejected"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="Reject a task after accepting",
    response_model_by_alias=True,
)
async def reject_task_after_acceptance(
    taskId: Annotated[StrictStr, Field(description="The ID of the task to reject")] = Path(..., description="The ID of the task to reject"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> RejectTaskAfterAcceptance200Response:
    """Allows a user to forfeit a task they previously accepted."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().reject_task_after_acceptance(taskId)


@router.post(
    "/tasks/{taskId}/validation",
    responses={
        200: {"model": TaskValidation200Response, "description": "Proof uploaded and under review"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        404: {"model": OpenDispute404Response, "description": "Task not found"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="Submit proof for task validation",
    response_model_by_alias=True,
)
async def task_validation(
    taskId: Annotated[StrictStr, Field(description="The ID of the task being validated")] = Path(..., description="The ID of the task being validated"),
    proof_video: Annotated[Optional[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]], Field(description="Screen recording file")] = Form(None, description="Screen recording file"),
    additional_notes: Annotated[Optional[StrictStr], Field(description="Optional notes about the proof")] = Form(None, description="Optional notes about the proof"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> TaskValidation200Response:
    """Allows the task doer to upload screen recording or relevant files for AI verification."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().task_validation(taskId, proof_video, additional_notes)


@router.post(
    "/tasks/{taskId}/validate",
    responses={
        200: {"model": ValidateTaskFinished200Response, "description": "Task successfully validated as completed"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        404: {"model": OpenDispute404Response, "description": "Task not found"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["tasks"],
    summary="Validate a task is finished",
    response_model_by_alias=True,
)
async def validate_task_finished(
    taskId: Annotated[StrictStr, Field(description="The ID of the task to validate as completed")] = Path(..., description="The ID of the task to validate as completed"),
    validate_task_finished_request: Optional[ValidateTaskFinishedRequest] = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ValidateTaskFinished200Response:
    """Allows the system or task creator to confirm the task is completed. Could be triggered by an admin or an automated AI service."""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().validate_task_finished(taskId, validate_task_finished_request)
