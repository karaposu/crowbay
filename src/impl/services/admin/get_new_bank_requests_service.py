import logging
from fastapi import HTTPException
from traceback import format_exc
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any

# from models.get_new_bank_requests200_response_inner import GetNewBankRequests200ResponseInner
# or however your response model is imported

logger = logging.getLogger(__name__)

class GetNewBankRequestsService:
    """
    Service class that retrieves new 'virgin bank' requests (this_is_a_virgin_bank == True)
    from InitialData, filtered by date range, country, etc.
    """

    def __init__(self, request, dependencies):
        self.request = request
        self.dependencies = dependencies
        self.response = None

        logger.debug("Inside GetNewBankRequestsService")

        self.preprocess_request_data()
        self.process_request()

    def preprocess_request_data(self):
        """
        1) Validate/parse request fields
        2) Access DB/Repository
        3) Retrieve the new bank requests
        4) Store data in self.preprocessed_data
        """
        try:
            # Extract parameters
            user_id = self.request.user_id  # Possibly not used for filtering, but we have it if needed
            country = self.request.country
            start_date = self.request.start_date
            end_date = self.request.end_date

            logger.debug(
                f"user_id={user_id}, country={country}, start_date={start_date}, end_date={end_date}"
            )

            # Provide default date range if none provided
            if not start_date:
                start_date = date.today().replace(year=date.today().year - 3)  # e.g., default to 1yr ago
                logger.debug(f"No start_date provided; defaulting to 1 year ago: {start_date}")
            if not end_date:
                end_date = date.today() + timedelta(days=1)  # up to tomorrow
                logger.debug(f"No end_date provided; defaulting to tomorrow: {end_date}")

            # Convert to datetime for DB queries
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(end_date, datetime.max.time())

            # Obtain DB session
            session_factory = self.dependencies.session_factory()
            session = session_factory()

            # Obtain repository
            # Suppose you have a method get_new_bank_requests in your admin_panel_report_repository
            admin_panel_report_repository_provider = self.dependencies.admin_panel_report_repository
            admin_repo = admin_panel_report_repository_provider(session=session)

            # Query the data
            requests_data = admin_repo.get_new_bank_requests(
                start_dt=start_dt,
                end_dt=end_dt,
                country=country
            )

            # Store results
            self.preprocessed_data = requests_data

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving new bank requests: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            # Close session if it was opened
            try:
                session.close()
            except:
                pass

    def process_request(self):
        """
        Convert raw data (list of dicts) to your Pydantic response model.
        """
        try:
            raw_data = getattr(self, "preprocessed_data", [])
            if not raw_data:
                logger.debug("No new bank requests found; returning empty list.")
                self.response = []
                return

            # If you have a Pydantic model `GetNewBankRequests200ResponseInner`, do something like:
            # final_output = []
            # for row in raw_data:
            #     model_item = GetNewBankRequests200ResponseInner(
            #         file_id=row["file_id"],
            #         new_bank_request_id=row["new_bank_request_id"],
            #         bank_name=row["bank_name"],
            #         country=row["country"],
            #         request_time=row["request_time"]
            #     )
            #     final_output.append(model_item)
            #
            # self.response = final_output

            # If your row structure matches your Pydantic model exactly, you might
            # do a direct parse. Otherwise, just return as dicts:
            self.response = raw_data

        except Exception as e:
            logger.error(f"Error building new bank requests response: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
