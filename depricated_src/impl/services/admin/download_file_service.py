# impl/services/admin/download_file_service.py

import logging
from datetime import datetime
from fastapi import HTTPException, Response
from traceback import format_exc

logger = logging.getLogger(__name__)

class DownloadFileService:
    def __init__(self, request, dependencies):
        """
        request: an object with attributes:
            - user_id (int)
            - file_id (int)
            - secret_key_for_file_download (any)
        dependencies: your DI container
        """
        self.request = request
        self.dependencies = dependencies
        self.response = None

        logger.debug("Inside DownloadFileService")

        # Step 1: gather all needed data
        self._preprocess_request_data()
        # Step 2: build the final Response
        self._process_request()

    # -------------------------------------------------------------------------
    # Private Helpers
    # -------------------------------------------------------------------------
    def _validate_secret_key(self):
        """Check if the provided secret key matches an expected value."""
        provided_secret = self.request.secret_key_for_file_download
        HARDCODED_ADMIN_SECRET = 123456  # or read from environment/config
        logger.debug(f"Provided secret={provided_secret}, expected={HARDCODED_ADMIN_SECRET}")

        if provided_secret != HARDCODED_ADMIN_SECRET:
            logger.error("Invalid secret key for file download.")
            raise HTTPException(
                status_code=403,
                detail="Forbidden: invalid secret key"
            )

    def _get_file_repository(self):
        """Obtain the FileRepository via dependencies and return it."""
        session_factory = self.dependencies.session_factory()
        session = session_factory()
        file_repository_provider = self.dependencies.file_repository
        file_repository = file_repository_provider(session=session)
        return file_repository, session

    def _fetch_file_data(self, file_repository) -> dict:
        """
        Calls `get_binary_file(...)` from the file repository,
        which returns a dictionary with raw_data_format, binary_data, encoded_raw_data, etc.
        """
        user_id = self.request.user_id
        file_id = self.request.file_id
        logger.debug(f"Fetching file data for user_id={user_id}, file_id={file_id}")

        file_data_dict = file_repository.get_binary_file(user_id, file_id)

        if not file_data_dict:
            logger.error(f"No file found with file_id={file_id} for user_id={user_id}")
            raise HTTPException(status_code=404, detail="File not found")

        return file_data_dict

    def _determine_content_type_and_filename(self, raw_data_format: str, file_id: int) -> (str, str):
        """
        Given a raw_data_format (pdf, xlsx, etc.) and file_id,
        decide on the content type & filename. 
        Returns (content_type, filename).
        """
        # Fallback defaults
        content_type = "application/octet-stream"
        filename = f"file_{file_id}"

        # Adjust logic based on your formats
        if raw_data_format.lower() in ["pdf"]:
            content_type = "application/pdf"
            filename += ".pdf"
        elif raw_data_format.lower() in ["xlsx", "xls", "csv"]:
            content_type = "application/vnd.ms-excel"  # or text/csv for CSV specifically
            filename += f".{raw_data_format.lower()}"
        # else keep the fallback

        return content_type, filename

    def _unify_binary_data(self, 
                           raw_data_format: str,
                           binary_data: bytes,
                           encoded_text: str) -> bytes:
        """
        Decide whether we use `binary_data` or decode `encoded_text`.
        Returns final bytes.
        """
        # If we have binary data, we can prioritize it
        if binary_data:
            return binary_data

        # Else if we have encoded text
        if encoded_text:
            # For PDF or other text-based storage in 'encoded_raw_data', decode from Latin-1
            if raw_data_format.lower() == "pdf":
                return encoded_text.encode("latin-1")
            # or add more logic as needed

        # If neither is present, we have an empty file
        return b""  # or None

    # -------------------------------------------------------------------------
    # Steps: Preprocess & Process
    # -------------------------------------------------------------------------
    def _preprocess_request_data(self):
        """
        1) Validate the secret_key_for_file_download
        2) Access the FileRepository
        3) Retrieve the file's data from DB
        4) Determine content type, filename, unify binary data
        5) Store in self.preprocessed_data
        """
        try:
            # 1) Validate secret
            self._validate_secret_key()

            # 2) Access the FileRepository
            file_repository, session = self._get_file_repository()

            # 3) Retrieve file data
            file_data_dict = self._fetch_file_data(file_repository)
            raw_format = file_data_dict.get("raw_data_format", "")
            raw_binary = file_data_dict.get("binary_data", None)
            encoded = file_data_dict.get("encoded_raw_data", None)

            # 4) Determine content type & filename
            content_type, filename = self._determine_content_type_and_filename(
                raw_data_format=raw_format,
                file_id=self.request.file_id
            )

            # 5) Unify binary data
            final_binary = self._unify_binary_data(
                raw_data_format=raw_format,
                binary_data=raw_binary,
                encoded_text=encoded
            )

            if not final_binary:
                logger.error("This file has no binary data stored.")
                raise HTTPException(status_code=404, detail="File contents empty")

            # Prepare for process_request
            self.preprocessed_data = {
                "binary_data": final_binary,
                "content_type": content_type,
                "filename": filename
            }

        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            logger.error(f"An error occurred during file retrieval: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def _process_request(self):
        """
        Return a FastAPI-compatible response with the file bytes as an attachment.
        """
        try:
            data = self.preprocessed_data
            file_bytes = data["binary_data"]
            ctype = data["content_type"]
            filename = data["filename"]

            from fastapi import Response  # or from starlette.responses
            headers = {
                "Content-Disposition": f'attachment; filename="{filename}"'
            }

            self.response = Response(
                content=file_bytes,
                media_type=ctype,
                headers=headers,
                status_code=200
            )

        except Exception as e:
            logger.error(f"Error building file response: {e}\n{format_exc()}")
            raise HTTPException(status_code=500, detail="Internal server error")
