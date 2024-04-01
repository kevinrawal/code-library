import sys
import os

from fastapi import APIRouter, HTTPException, status
from jose import JWTError, jwt

from models.folders import Folder
from services.folder_services import (
    get_folder_from_db,
    search_folder_by_name_from_db,
    add_folder_in_db,
    update_folder_in_db,
    delete_folder_from_db,
)

# THIS CODE IS TO ACCESS MODULES OUTSIDE ROUTE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def authorize_user_by_user_id(user_id: str, token: str) -> bool:
    """Authorize user based on user_id

    Args:
        user_id (str): _description_
        token (str): _description_

    Returns:
        bool: _description_
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_from_token = payload.get("user_id")
        return user_id_from_token == user_id
    except JWTError:
        return False

def authorize_user_via_email(email_id: str, token: str) -> bool:
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

@router.get("/folder-by-id", status_code=status.HTTP_200_OK)
async def get_folder_by_id(folder_id: str, token: str):
    """Get folder by it's _id 

    Args:
        folder_id (str): _id of folder from folders collection
        token (str): jwt token

    Raises:
        HTTPException: _description_
        credentials_exception: _description_

    Returns:
        _type_: _description_
    """

    folder = await get_folder_from_db(folder_id)

    if folder is not None and authorize_user_by_user_id(folder["user_id"], token):
        return folder
    elif folder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such folder exist"
        )
    else:
        raise credentials_exception


@router.get("/folder-by-name", status_code=status.HTTP_200_OK)
async def search_folder_by_name(folder_name: str, token: str):
    """search folder by it's name, this function return all the matching folder with user_id in token

    Args:
        folder_name (str): _description_
        token (str): _description_

    Raises:
        credentials_exception: _description_

    Returns:
        _type_: _description_
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return await search_folder_by_name_from_db(folder_name, user_id)
    except JWTError:
       raise credentials_exception


@router.post("/folder", status_code=status.HTTP_200_OK)
async def create_folder(folder: Folder, token: str):
    """Create new folder in database based on user_id from token

    Args:
        folder (Folder): _description_
        token (str): _description_

    Raises:
        credentials_exception: _description_
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        folder.user_id = user_id
        await add_folder_in_db(folder)
    except JWTError:
       raise credentials_exception


@router.put("/folder", status_code=status.HTTP_200_OK)
async def update_folder(folder_id: str,folder: Folder, token: str):
    """Update folder"""
    #TODO - need more security 

    if authorize_user_by_user_id(folder.user_id, token):
        await update_folder_in_db(folder_id,folder)
    else:
        raise credentials_exception


@router.delete("/folder", status_code=status.HTTP_200_OK)
async def delete_folder(folder_id: str, token: str):
    """Delete folder"""

    folder = await get_folder_from_db(folder_id)
    if folder is not None and authorize_user_by_user_id(folder["user_id"],token):
        await delete_folder_from_db(folder_id)
    else:
        raise credentials_exception

