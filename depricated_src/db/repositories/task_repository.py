# db/repositories/task_repository.py

import logging
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import Task, User
from models.create_task_request import CreateTaskRequest
from models.create_task201_response import CreateTask201Response

logger = logging.getLogger(__name__)

class TaskRepository:
    """
    Repository class for CRUD operations on 'Task' objects.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_new_task(self, user_id: int, new_task_request: CreateTaskRequest) -> CreateTask201Response:
        """
        Creates a new Task in the database for the specified user.

        :param user_id: The ID of the user creating the task.
        :param new_task_request: The incoming CreateTaskRequest with task details.
        :return: A CreateTask201Response containing the new task ID and a success message.
        """
        try:
            # 1. Check if the user exists
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # 2. Create a new Task object
            new_task = Task(
                owner_id=user.id,
                desc=new_task_request.desc,
                total_budget=new_task_request.total_budget or 0.0,
                you_earn=new_task_request.you_earn or 0.0,
                partition_deadline=new_task_request.partition_deadline,
                submission_deadline=new_task_request.submission_deadline,
                category=new_task_request.category,
                bay_review=new_task_request.bay_review or False
            )

            # 3. Add and flush to assign an ID
            self.session.add(new_task)
            self.session.flush()  # flush() so that new_task.id is generated immediately

            # 4. Build a response
            response = CreateTask201Response(
                task_id=str(new_task.id),
                msg="Task created."
            )

            return response

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating task: {str(e)}")
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Database error while creating task")

        except HTTPException as he:
            # If it's already an HTTPException (e.g., user not found),
            # just re-raise after rolling back, so the caller can handle it.
            logger.error(f"HTTPException: {he.detail}")
            self.session.rollback()
            raise he

        except Exception as e:
            logger.error(f"Unknown error while creating task: {str(e)}")
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Unknown error while creating task")
