# db/repositories/base_user_validation_repository.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from fastapi import HTTPException
import logging
import pandas as pd
from typing import List, Optional

# from db.models import ProcessedData, InitialData
# from models.split_record_dto import SplitRecordDTO

from sqlalchemy import or_

logger = logging.getLogger(__name__)

class BaseUserValidationRepository:
    def __init__(self, session: Session):
        self.session = session
