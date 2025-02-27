# coding: utf-8
# wallet_api.py


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
from pydantic import Field, StrictStr, field_validator
from typing import List, Optional
from typing_extensions import Annotated
from models.add_balance200_response import AddBalance200Response
from models.add_balance400_response import AddBalance400Response
from models.add_balance401_response import AddBalance401Response
from models.add_balance500_response import AddBalance500Response
from models.add_balance_request import AddBalanceRequest
from models.transaction_history200_response_inner import TransactionHistory200ResponseInner
from models.withdraw_money200_response import WithdrawMoney200Response
from models.withdraw_money_request import WithdrawMoneyRequest
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
    "/wallet/add-balance",
    responses={
        200: {"model": AddBalance200Response, "description": "Balance deposit details"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["wallet"],
    summary="Add balance to user account",
    response_model_by_alias=True,
)
async def add_balance(
    add_balance_request: AddBalanceRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AddBalance200Response:
    """Allows a user to deposit funds (e.g., USDT, PEPE) into their platform wallet."""
    if not BaseWalletApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWalletApi.subclasses[0]().add_balance(add_balance_request)


@router.get(
    "/wallet/transactions",
    responses={
        200: {"model": List[TransactionHistory200ResponseInner], "description": "A list of user transactions"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["wallet"],
    summary="Get transaction history",
    response_model_by_alias=True,
)
async def transaction_history(
    status: Annotated[Optional[StrictStr], Field(description="Optional filter by transaction status")] = Query(None, description="Optional filter by transaction status", alias="status"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[TransactionHistory200ResponseInner]:
    """Returns a list of all deposit and withdrawal transactions for the authenticated user."""
    if not BaseWalletApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWalletApi.subclasses[0]().transaction_history(status)


@router.post(
    "/wallet/withdraw",
    responses={
        200: {"model": WithdrawMoney200Response, "description": "Withdrawal processed successfully"},
        400: {"model": AddBalance400Response, "description": "Bad Request"},
        401: {"model": AddBalance401Response, "description": "Unauthorized"},
        500: {"model": AddBalance500Response, "description": "Internal Server Error"},
    },
    tags=["wallet"],
    summary="Withdraw money from user account",
    response_model_by_alias=True,
)
async def withdraw_money(
    withdraw_money_request: WithdrawMoneyRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> WithdrawMoney200Response:
    """Allows a user to withdraw funds (e.g., USDT, PEPE) from their platform wallet."""
    if not BaseWalletApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWalletApi.subclasses[0]().withdraw_money(withdraw_money_request)
