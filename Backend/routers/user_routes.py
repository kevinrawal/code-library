"""user routes"""

import sys
import os

from fastapi import APIRouter, HTTPException, status
from jose import JWTError, jwt

from models.users import User
from services.user_services import (
    create_user_in_db,
    update_password_in_db,
    update_email_in_db,
    delete_user_from_db,
)

# THIS CODE IS TO ACCESS MODULES OUTSIDE ROUTE AND APP FOLDER
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
)

router = APIRouter()


async def authorize_user_via_email(email_id: str, token: str) -> bool:
    """Authorize user based on email id

    Args:
        email_id (str): _description_
        token (str): _description_

    Returns:
        bool: status
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_id_from_token = payload.get("email_id")
        return email_id == email_id_from_token
    except JWTError:
        return False


@router.post("/user", status_code=status.HTTP_200_OK)
async def create_user(user: User):
    """Create new user in users collection

    Args:
        user (User): contain email_id and password

    Raises:
        HTTPException: if user is already exist
    """

    await create_user_in_db(user)
    return {"message": "User created successfully"}


@router.put("/user-password", status_code=status.HTTP_200_OK)
async def update_password(user: User, token: str):
    """Update password in users collection"""
    if authorize_user_via_email(user.email_id, token) is False:
        raise credentials_exception

    await update_password_in_db(user.email_id, user.password)
    return {"message": "Password updated sucessfully"}

@router.put("/user-email", status_code=status.HTTP_200_OK)
async def update_email(prev_email_id: str, new_email_id: str, token: str):
    """Update email in users collectiom"""
    if authorize_user_via_email(prev_email_id, token) is False:
        raise credentials_exception

    await update_email_in_db(prev_email_id, new_email_id)
    return {"message": "Eamail updated successfully"}

@router.delete("/user", status_code=status.HTTP_200_OK)
async def delete_user(email_id: str, token: str):
    """Delete user in users collection"""
    if authorize_user_via_email(email_id, token) is False:
        raise credentials_exception

    await delete_user_from_db(email_id)
    return {"message": "user deleted successfully"}