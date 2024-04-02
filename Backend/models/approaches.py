"""Approaches defination"""

from pydantic import BaseModel


class Approaches(BaseModel):
    """Approaches are the important part of code blocks
    they contain information for a perticular approach

    Args:
        BaseModel (_type_): _description_
    """

    logic: str = ""
    code_info: dict = {"code": "", "language": "c++"}
    time_complexity: str = ""
    space_complexity: str = ""
