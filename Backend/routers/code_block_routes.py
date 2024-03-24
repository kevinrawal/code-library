import sys
import os

from fastapi import APIRouter, HTTPException, status
from jose import JWTError, jwt

from models.code_blocks import CodeBlock
from services.code_block_services import (
    add_code_block_in_db,
    get_code_block_from_db,
    search_code_block_from_db,
    update_code_block_in_db,
    delete_code_block_from_db
)
# THIS CODE IS TO ACCESS MODULES OUTSIDE ROUTE AND
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
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
        email_id_from_token: str = payload.get("email_id")
        return email_id == email_id_from_token
    except JWTError:
        return False

@router.post("/code-block", status_code=status.HTTP_200_OK)
def create_code_block(code_block: CodeBlock, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        code_block.user_id = user_id
        add_code_block_in_db(code_block)
    except JWTError:
       raise credentials_exception

@router.get("/code-block-by-id", status_code=status.HTTP_200_OK)
def get_code_block_by_id(code_block_id: str, token: str):
    code_block = get_code_block_from_db(code_block_id)

    if code_block is not None and authorize_user_by_user_id(code_block["user_id"],token):
        return code_block
    elif code_block is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="code block not exist")
    else:
        raise credentials_exception
    
@router.get("/code-block-by-name", status_code=status.HTTP_200_OK)
def get_code_block_by_name(code_block_name: str, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return search_code_block_from_db(code_block_name, user_id)
    except JWTError:
        raise credentials_exception
    
@router.put("/code-block", status_code=status.HTTP_200_OK)
def update_code_block(code_block_id: str, code_block: CodeBlock, token: str):
    if authorize_user_by_user_id(code_block.user_id, token):
        update_code_block_in_db(code_block_id,code_block)
    else:
        raise credentials_exception
    
@router.delete("/code-block", status_code=status.HTTP_200_OK)
def delete_code_block(code_block_id: str, token: str):
    code_block = get_code_block_from_db(code_block_id)
    if code_block is not None and authorize_user_by_user_id(code_block["user_id"],token):
        delete_code_block_from_db(code_block_id)
    else:
        raise credentials_exception