"""Users defination"""

from pydantic import BaseModel


class User(BaseModel):
    """This is user module, it  is used to create user object,
    in database there is one more filed _id, which is assing by the system
    """

    email_id: str
    password: str
