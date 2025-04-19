# here is core/containers.py
from dependency_injector import containers, providers

import logging
logger = logging.getLogger(__name__)
import os


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from db.repositories.user_repository import UserRepository
# from db.repositories.file_repository import FileRepository
from db.session import get_engine
import yaml

from db.repositories.base_user_validation_repository import BaseUserValidationRepository
# from db.repositories.payment_repository import 
from db.repositories.task_repository import TaskRepository
from db.repositories.user_repository import UserRepository


# from db.repositories.report_repository import ReportRepository

# from utils.currency_utils import load_currency_configs

class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Engine provider
    engine = providers.Singleton(
        create_engine,
        config.db_url,
        echo=False
    )

    # # Session factory provider
    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine
    )

    task_repository_provider = providers.Factory(
        TaskRepository,
        session=providers.Dependency()
    )

    
    user_repository_provider = providers.Factory(
        UserRepository,
        session=providers.Dependency()
    )


    base_validation_repository_provider = providers.Factory(
        BaseUserValidationRepository,
        session=providers.Dependency()
    )




    



