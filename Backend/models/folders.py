from pydantic import BaseModel


class Folder(BaseModel):
    user_id: str
    folder_name: str
    parent_folder_id: str
    child_folders: list = []
    child_code_blocks: list = []
