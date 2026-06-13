# impl/services/admin/get_file_report_linechart_service.py

import logging
from fastapi import HTTPException
from traceback import format_exc
from datetime import datetime, date
from typing import Optional, Any

# Suppose this is your response model from the line chart endpoint
# e.g. from models.get_file_report_linechart200_response_inner import GetFileReportLinechart200ResponseInner
# from models.get_file_report_linechart200_response_inner import GetFileReportLinechart200ResponseInner

logger = logging.getLogger(__name__)

class GetFileReportLinechartService:
    """
    Service class that retrieves line chart data for file reports
    based on period_type, date range, country, bank, status, etc.
    """

    def __init__(self, request, dependencies):
        self.request = request
        self.dependencies = dependencies
        self.response = None

        logger.debug("Inside GetFileReportLinechartService")
        
        self.preprocess_request_data()
        self.process_request()
    
    def preprocess_request_data(self):
        """
        1) Validate or parse request fields
        2) Access the DB/Repository
        3) Aggregate line chart data
        4) Store data in self.preprocessed_data
        """
        try:
            # Extract parameters
            user_id = self.request.user_id
            period_type = self.request.period_type
            start_date = self.request.start_date  # possibly a datetime.date
            end_date = self.request.end_date      # possibly a datetime.date
            country = self.request.country
            bank_id = self.request.bank_id
            status = self.request.status

            logger.debug(f"user_id={user_id}, period_type={period_type}, "
                         f"start_date={start_date}, end_date={end_date}, "
                         f"country={country}, bank_id={bank_id}, status={status}")

            # 1) Basic validation / normalization:
            #    Example: if period_type not in ["day", "week", "month", "year"], raise error
            valid_periods = {"day", "week", "month", "year"}
            if period_type not in valid_periods:
                logger.error(f"Invalid period_type: {period_type}")
                raise HTTPException(status_code=400, detail="Invalid period_type parameter")

            # Convert date objects to datetime if needed, or ensure they have default values
            if not start_date:
                # fallback, e.g. 10 year ago
                start_date = date.today().replace(year=date.today().year - 10)
            if not end_date:
                from datetime import datetime, timedelta
                end_date = date.today() + timedelta(days=11)
                

            # 2) Access a DB session
            session_factory = self.dependencies.session_factory()
            session = session_factory()

            # 3) Access a repository that can fetch line-chart data
            #    Suppose we have "admin_panel_report_repository"
            admin_panel_report_repository_provider = self.dependencies.admin_panel_report_repository
            admin_repo = admin_panel_report_repository_provider(session=session)
            
            # 4) Query data. We'll define a (hypothetical) repository method:
            #    e.g. admin_repo.get_file_report_linechart(...)
            linechart_data = admin_repo.get_file_report_linechart(
                period_type=period_type,
                start_date=start_date,
                end_date=end_date,
                country=country,
                bank_id=bank_id,
                status=status
            )
            # linechart_data might be a list of dicts or rows.

            # Store your aggregated data
            self.preprocessed_data = linechart_data

        except HTTPException:
            # re-raise fastapi's HTTPException
            raise
        except Exception as e:
            logger.error(f"An error occurred while retrieving line chart data: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            # If you opened a session, close it here
            try:
                session.close()
            except:
                pass

    def process_request(self):
        """
        Format the final output data (in the shape of your Pydantic response model).
        """
        # Suppose your repository returned a list of dicts with keys like "date", "count"
        # or something more complex. You might need to transform them here into
        # the `GetFileReportLinechart200ResponseInner` models.
        try:
            raw_data = getattr(self, "preprocessed_data", [])
            if not raw_data:
                # Could return empty list
                logger.debug("No line chart data found, returning empty list.")
                self.response = []
                return

            # Transform each row/dict into your Pydantic output model
            # For example, if your model has fields: date_str, value, etc.
            # from models.get_file_report_linechart200_response_inner import GetFileReportLinechart200ResponseInner

            # final_output = []
            # for row in raw_data:
            #     # row might have e.g. row["some_date"], row["some_value"]
            #     # Convert that to your pydantic model
            #     item = GetFileReportLinechart200ResponseInner(
            #         date_str=row["some_date_str"],
            #         count=row["some_aggregate_count"]
            #         # etc.
            #     )
            #     final_output.append(item)

            # self.response = final_output

            # For now, if you just want to return the raw data (assuming it matches the Pydantic schema):
            logger.debug(f"raw_data: {raw_data}")
            self.response = raw_data

        except Exception as e:
            logger.error(f"Error building line chart response: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
