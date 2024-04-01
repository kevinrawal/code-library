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

#TODO - solve re-raising error in all below methods 
@router.post("/code-block", status_code=status.HTTP_200_OK)
async def create_code_block(code_block: CodeBlock, token: str):
    """Create new code block in code_blocks collection

    Args:
        code_block (CodeBlock): _description_
        token (str): _description_

    Raises:
        credentials_exception: _description_
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        code_block.user_id = user_id
        await add_code_block_in_db(code_block)
    except JWTError:
       raise credentials_exception

@router.get("/code-block-by-id", status_code=status.HTTP_200_OK)
async def get_code_block_by_id(code_block_id: str, token: str):
    """return code block of given id from code_blocks collection

    Args:
        code_block_id (str): _description_
        token (str): _description_

    Raises:
        HTTPException: _description_
        credentials_exception: _description_

    Returns:
        _type_: _description_
    """

    code_block = await get_code_block_from_db(code_block_id)

    if code_block is not None and authorize_user_by_user_id(code_block["user_id"],token):
        return code_block
    elif code_block is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="code block not exist")
    else:
        raise credentials_exception

@router.get("/code-block-by-name", status_code=status.HTTP_200_OK)
async def get_code_block_by_name(code_block_name: str, token: str):
    """Return code blocks of query name for current user

    Args:
        code_block_name (str): _description_
        token (str): _description_

    Raises:
        credentials_exception: _description_
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return await search_code_block_from_db(code_block_name, user_id)
    except JWTError:
        raise credentials_exception

@router.put("/code-block", status_code=status.HTTP_200_OK)
async def update_code_block(code_block_id: str, code_block: CodeBlock, token: str):
    """Update code block in code blocks collection

    Args:
        code_block_id (str): _description_
        code_block (CodeBlock): _description_
        token (str): _description_

    Raises:
        credentials_exception: _description_
    """

    if authorize_user_by_user_id(code_block.user_id, token):
        await update_code_block_in_db(code_block_id,code_block)
    else:
        raise credentials_exception

@router.delete("/code-block", status_code=status.HTTP_200_OK)
async def delete_code_block(code_block_id: str, token: str):
    """Delete code block from the code_blocks collection 

    Args:
        code_block_id (str): _description_
        token (str): _description_

    Raises:
        credentials_exception: _description_
    """
    
    code_block = await get_code_block_from_db(code_block_id)

    print(code_block)
    if code_block is not None and authorize_user_by_user_id(code_block["user_id"],token):
        await delete_code_block_from_db(code_block_id)
    else:
        print("credential")
        raise credentials_exception