# services/tasks/create_task.py

import logging
from fastapi import HTTPException
from traceback import format_exc

from impl.utils import create_db_session

from models.create_task_request import CreateTaskRequest
from models.create_task201_response import CreateTask201Response




logger = logging.getLogger(__name__)
# life is in essence is pain that never ends. And in some moments we are relieved fron this pain just a little but and we call this 
# moements happyness. Yet they are far from it. No true happyness in this life for me. I never had luck it with. 
# if you say you are truly happy then i wont believe you are human after all. to be is to suffer. And I exist. 

class CreateTaskService:
    def __init__(self, user_id: int, request: CreateTaskRequest, dependencies):
        """ 
        :param user_id: The user's ID making the buy request
        :param request: The full buy-pepecoin order request (fe_incall_time, give, take, etc.)
        :param dependencies: DI container with your repository providers
        """
        self.request = request
        self.user_id = user_id
        self.dependencies = dependencies
        self.response: CreateTask201Response = None
        logger.debug("Inside CreateTaskService")
        self.preprocess_request_data()
        self.process_request()
        
    def preprocess_request_data(self):
        logger.debug("Inside preprocess_request_data")
        
        # You can do additional checks/manipulations here if needed.
        # For example:
        # if not self.request.give_amount and not self.request.take_amount:
        #     raise HTTPException(status_code=400, detail="Must specify either give_amount or take_amount.")

        try:
            session = create_db_session(self.dependencies)
            
            try:
                logger.debug("Now inside the database session")
                
                # Create the repository with the session
                task_repository = self.dependencies.task_repository_provider(session=session)
                logger.debug("buypepecoin_repository created")

                # Save the buy request to the DB; 
                # this method now returns a BuyPepecoinOrderPost200Response.
                create_task_response = task_repository.create_new_task( user_id=self.user_id,
                    new_task_request=self.request
                )

                # Store that in self.preprocessed_data (or directly in self.response)
                self.preprocessed_data = create_task_response

                session.commit()

            except HTTPException as http_exc:
                session.rollback()
                logger.error(f"HTTPException during buy-pepecoin save: {http_exc.detail}")
                raise http_exc

            except Exception as e:
                session.rollback()
                logger.error(f"An error occurred while saving the buy-pepecoin request: {e}\n{format_exc()}")
                raise HTTPException(status_code=500, detail="Internal server error")
            
            finally:
                session.close()

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    def process_request(self):
        # We’ll just assign the "order_response" from the DB to our final response.
        self.response = self.preprocessed_data
