"""Model defination for code blocks"""

from pydantic import BaseModel


class CodeBlock(BaseModel):
    """CodeBlock is Component of Code Library

    Args:
        BaseModel (_type_): _description_
    """

    user_id: str
    code_block_name: str = "Untitled CodeBlock"
    parent_folder_id: str
    problem_statement: str = ""
    approaches: list = []
    similar_questions: list = []


class UpdateCodeBlock(BaseModel):
    """Class used as request body to update code block

    Args:
        BaseModel (_type_): _description_
    """

    user_id: str
    code_block_id: str
    code_block_name: str = "Untitled CodeBlock"
    problem_statement: str = ""
    approaches: list = []
    similar_questions: list = []
