#impl/services/admin/get_users_list_service.py

import logging
from fastapi import HTTPException
from traceback import format_exc

logger = logging.getLogger(__name__)

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GetUsersListService:
    def __init__(self, request, dependencies):
        self.request = request
        self.dependencies = dependencies
        self.response = None

        logger.debug("Inside GetUsersListService")

        self.preprocess_request_data()
        self.process_request()

    def preprocess_request_data(self):
        # Extract fields from the request object
        page = self.request.page
        page_size = self.request.page_size
        filter_country = self.request.country
        filter_user_id = self.request.user_id
        filter_email = self.request.email
        sort_by = self.request.sort_by
        sort_order = self.request.sort_order

        if page is None:
            page=0
        if page_size is None:
            page_size=5

        logger.debug("Inside preprocess_request_data")
        logger.debug(f"Filter user_id (from request): {filter_user_id}")
        logger.debug(f"Filter country: {filter_country}")
        logger.debug(f"Sort by: {sort_by}, sort order: {sort_order}")

        try:
            # Access session_factory and AdminPanelUserRepository from dependencies
            logger.debug("Accessing session_factory and admin_panel_user_repository providers")
            session_factory = self.dependencies.session_factory()
            admin_panel_user_repository_provider = self.dependencies.admin_panel_user_repository

            # Create a new database session
            session = session_factory()
            try:
                logger.debug("Now inside the database session")
                # Instantiate the AdminPanelUserRepository with the session
                admin_panel_user_repository = admin_panel_user_repository_provider(session=session)
                
                # Retrieve the user list
                logger.debug("Retrieving user list from admin_panel_user_repository...")
                users_data = admin_panel_user_repository.get_user_list_with_pagination(
                    page=page,
                    page_size=page_size,
                    filter_country=filter_country,
                    filter_user_id=filter_user_id,
                    filter_email=filter_email,
                    sort_by=sort_by,
                    sort_order=sort_order
                )

                logger.debug(f"Users data retrieved: {users_data}")

                # Store in preprocessed_data so process_request() can finalize it
                self.preprocessed_data = users_data

            except Exception as e:
                session.rollback()
                logger.error(f"An error occurred during user retrieval: {e}\n{format_exc()}")
                raise HTTPException(status_code=500, detail="Internal server error")

            finally:
                session.close()

        except HTTPException as http_exc:
            # Re-raise HTTP exceptions to be handled by FastAPI
            raise http_exc

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def process_request(self):
        # Prepare the response
        self.response = self.preprocessed_data
