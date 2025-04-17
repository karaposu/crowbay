import logging
from fastapi import HTTPException
from traceback import format_exc
from datetime import date, datetime, timedelta
from typing import Optional

# If your response model is something like this:
# from models.get_file_report_total200_response import GetFileReportTotal200Response

logger = logging.getLogger(__name__)

class GetFileReportTotalService:
    """
    Service class that retrieves overall file statistics (totals)
    based on date range, country, bank, status, etc.
    """

    def __init__(self, request, dependencies):
        self.request = request
        self.dependencies = dependencies
        self.response = None

        logger.debug("Inside GetFileReportTotalService")

        self.preprocess_request_data()
        self.process_request()

    def preprocess_request_data(self):
        """
        1) Validate/parse request fields
        2) Access the DB/Repository
        3) Aggregate the total file stats
        4) Store data in self.preprocessed_data
        """
        try:
            # Extract parameters from the request
            user_id = self.request.user_id
            start_date = self.request.start_date  # possibly None
            end_date = self.request.end_date      # possibly None
            country = self.request.country
            bank_id = self.request.bank_id
            status = self.request.status

            logger.debug(
                f"user_id={user_id}, "
                f"start_date={start_date}, end_date={end_date}, "
                f"country={country}, bank_id={bank_id}, status={status}"
            )

            # 1) Provide default date range if none
            if not start_date:
                # Example: default start ~1 year ago (or 10 years, up to you)
                start_date = date.today().replace(year=date.today().year - 1)
                logger.debug(f"No start_date given; defaulting to ~1 year ago: {start_date}")
            if not end_date:
                end_date = date.today() + timedelta(days=1)
                logger.debug(f"No end_date given; defaulting to tomorrow: {end_date}")

            # Convert them to datetime for DB comparison
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(end_date, datetime.max.time())

            # 2) Access DB session
            session_factory = self.dependencies.session_factory()
            session = session_factory()

            # 3) Access your repository that can fetch totals
            #    Suppose we call it "admin_panel_report_repository"
            admin_panel_report_repository_provider = self.dependencies.admin_panel_report_repository
            admin_repo = admin_panel_report_repository_provider(session=session)

            # 4) Query the totals
            #    We'll define a new method: admin_repo.get_file_report_total(...)
            #    that returns a dict like:
            #    {
            #      "total_files": X,
            #      "processed_files": Y,
            #      "failed_files": Z,
            #      ...maybe other data...
            #    }
            results = admin_repo.get_file_report_total(
                start_dt=start_dt,
                end_dt=end_dt,
                country=country,
                bank_id=bank_id,
                status=status
            )

            # Store the result
            self.preprocessed_data = results

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving total file report: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            # Close session if it was opened
            try:
                session.close()
            except:
                pass

    def process_request(self):
        """Wrap the raw data into the final Pydantic response model."""
        try:
            raw_data = getattr(self, "preprocessed_data", {})
            if not raw_data:
                # Provide a default structure if no data
                logger.debug("No file totals found; returning empty structure.")
                raw_data = {
                    "total_files": 0,
                    "processed_files": 0,
                    "failed_files": 0
                    # etc.
                }

            # If you have a Pydantic model, do something like:
            # response_model = GetFileReportTotal200Response(**raw_data)
            # self.response = response_model

            # If returning directly as a dict:
            self.response = raw_data

        except Exception as e:
            logger.error(f"Error building total file report response: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
