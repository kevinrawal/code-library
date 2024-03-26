"""User Services, contain functions to intract with database"""

import os
import sys
import re

from fastapi import HTTPException, status
from passlib.context import CryptContext
from config.database import user_db
from models.users import User
from models.folders import Folder


from services.folder_services import add_folder_in_db, delete_folder_from_db_by_id
from services.code_block_services import delete_code_block_from_db_by_id

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class custom_exception(Exception):
    pass


def validate_email_id(email_id: str):
    """Validate email"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email_id))


def validate_password_constrain(password: str):
    """check password validation"""
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$"
    return bool(re.match(pattern, password))


def get_password_hash(password):
    """Generate hash password from plain password"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Verify plain password with hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_user_from_db(email_id: str) -> dict:
    """Return user of userid as dictionary or none if user not exist"""
    user = user_db.find_one({"email_id": email_id})
    if user is not None:
        # changing the type of _id from ObjectId to string
        user["_id"] = str(user["_id"])

    return user


def create_user_in_db(user: User):
    """Create new user in users collection,
    creare root folder for that user

    Args:
        user (User): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
    """
    if user_db.find_one({"email_id": user.email_id}) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already exist"
        )

    if validate_email_id(user.email_id) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid email"
        )

    if validate_password_constrain(user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="weak password"
        )

    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    # _id is created by system wich is of type ObjectId
    # ObjectId is of 12 byte while str is of 24 so better to use ObjectId

    # create user and root folder for the user, user can not delete the root folder
    response = user_db.insert_one(user_dict)
    user_id = str(response.inserted_id)
    root_folder = Folder(user_id=user_id, folder_name="~", parent_folder_id="-1")
    add_folder_in_db(root_folder)


def delete_user_from_db(email_id: str) -> bool:
    """Delete user from users collection,
    also delete all it's folder and code blocks from the database

    Args:
        email_id (str): email of user

    Returns:
        bool: status
    """
    user = get_user_from_db(email_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    user_id = user["_id"]
    user_db.delete_one({"email_id": email_id})
    # delete all data associated with user
    delete_folder_from_db_by_id(user_id)
    delete_code_block_from_db_by_id(user_id)

    # TODO - above function should run asynchronously


def update_password_in_db(email_id: str, new_password: str) -> bool:
    """Update password in the Database

    Args:
        email_id (str): email of user
        new_password (str): new password

    Returns:
        bool: _description_
    """
    user = get_user_from_db(email_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    if validate_password_constrain(new_password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="weak password"
        )

    filter_match = {"email_id": email_id}
    update = {"$set": {"password": get_password_hash(new_password)}}
    user_db.update_one(filter_match, update)
    return True


def update_email_in_db(prev_email_id: str, new_email_id: str) -> bool:
    """Update Email id in users collection

    Args:
        prev_email_id (str): existing email id
        new_email_id (str): email to set

    Returns:
        bool: status
    """
    user = get_user_from_db(prev_email_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    if validate_email_id(new_email_id) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email"
        )

    filter_match = {"email_id": prev_email_id}
    update = {"$set": {"email_id": new_email_id}}
    user_db.update_one(filter_match, update)
    return True
