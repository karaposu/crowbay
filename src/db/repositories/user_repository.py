# db/repositories/user_repository.py
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext
import logging

from db.models import User
from typing import Optional

logger = logging.getLogger(__name__)



'''

korkuluk


{
  "desc": "string",
  "expected_result_explanation"
  "total_budget": 0,
  "per_crow_budget": 0,
   num_of_crows :
  "task_halving" integer which signifies how many days after task is published, the halving will occur. default is 15, once the halving 
  occurs, per_crow_budget is doubled.  task_halving is used for tasks where it is hard to find users. 
  "
  partition_deadline": "2025-03-03T20:32:14.906Z",
  "submission_deadline": "2025-03-03T20:32:14.906Z",
   
  "example_validation_video"
  
  "bay_review": true,
  "filters": {
    "city": "string",
    "demographic": "string"
  }
}


first location filter will be prompt to the user


user must be able to pick fast 

"minsk" and "istanbul" 

"EMEA"

"not india"



'''

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def add_new_user(self, email: str, hashed_password: str) -> int:
        try:
            db_user = User(
                email=email,
                password_hash=hashed_password,
                created_at=datetime.utcnow(),
                name=""  # Set name if needed
            )
            self.session.add(db_user)
            self.session.commit()
            return db_user.id
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error adding new user: {str(e)}")
            raise HTTPException(status_code=500, detail="Error adding new user")
    
    def get_user_by_email(self, email: str) -> User:
        try:
            logger.debug(f"filtering db with the email..")
            db_user = self.session.query(User).filter(User.email == email).first()
            return db_user
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Database error: {e}")
            return None
    
    def check_user_by_email(self, email: str) -> bool:
        logger.debug(f"inside the    check_user_by_email")
        db_user = self.get_user_by_email(email)
        return db_user is not None

    def change_password(self, email: str, new_password: str):
        user = self.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        new_hashed_password = self.pwd_context.hash(new_password)
        user.password_hash = new_hashed_password
        self.session.add(user)
        self.session.commit()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def make_user_verified_from_email(self, email: str):
        db_user = self.get_user_by_email(email)
        if db_user:
            db_user.is_verified = True
            self.session.add(db_user)
            self.session.commit()

    def add_default_currency(self, user_id: int, default_currency: str):
        try:
            user_settings = self.session.query(UserSettings).filter_by(user_id=user_id).first()

            if user_settings:
                # Update existing settings
                user_settings.default_currency = default_currency
            else:
                # Create new settings entry
                user_settings = UserSettings(
                    user_id=user_id,
                    default_currency=default_currency
                )
                self.session.add(user_settings)

            self.session.commit()
            logger.info(f"Set default currency for user_id {user_id} to {default_currency}")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error setting default currency for user_id {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error setting default currency")



    def update_user_settings(self, user_id: int, **kwargs):
        try:
            user_settings = self.session.query(UserSettings).filter_by(user_id=user_id).first()

            # Get all column names from the UserSettings model, excluding primary keys and foreign keys
            mapper = inspect(UserSettings)
            primary_keys = {column.key for column in mapper.primary_key}
            foreign_keys = {column.key for column in mapper.columns if column.foreign_keys}
            excluded_fields = primary_keys.union(foreign_keys)
            allowed_fields = set(mapper.columns.keys()).difference(excluded_fields)

            # Filter kwargs to only include allowed fields
            update_fields = {key: value for key, value in kwargs.items() if key in allowed_fields}

            if not update_fields:
                raise ValueError("No valid settings provided to update.")

            if user_settings:
                # Update existing settings
                for key, value in update_fields.items():
                    setattr(user_settings, key, value)
            else:
                # Create new settings entry
                user_settings = UserSettings(
                    user_id=user_id,
                    **update_fields
                )
                self.session.add(user_settings)

          

            self.session.commit()
            logger.info(f"Updated settings for user_id {user_id} with {update_fields}")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating settings for user_id {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error updating user settings")
        except ValueError as ve:
            logger.error(f"Invalid update attempt for user_id {user_id}: {str(ve)}")
            raise HTTPException(status_code=400, detail=str(ve))
    
   