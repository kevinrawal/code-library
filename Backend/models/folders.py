"""Folders Defination"""

from pydantic import BaseModel


class Folder(BaseModel):
    """Folders are containers contains code blocks and other folders 

    Args:
        BaseModel (_type_): _description_
    """
    user_id: str
    folder_name: str = "Untitled Folder"
    parent_folder_id: str
    child_folders: list = []
    child_code_blocks: list = []