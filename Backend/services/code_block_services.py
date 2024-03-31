import os
import sys
from bson.objectid import ObjectId

from fastapi import HTTPException, status

from config.database import code_blocks_db,folders_db
from models.code_blocks import CodeBlock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def add_code_block_in_db(code_block: CodeBlock):
    """Add new Code block in code_block collection
       it automatically assing new _id t this code block which is of ObjectId type
    Args:
        code_block (CodeBlock): _description_
    """

    # convert code block into dictionary and then add to the code_blocks_db collection
    code_block_dict = code_block.model_dump()
    response = code_blocks_db.insert_one(code_block_dict)

    # add this code block id into it's parent child_code_blocks list 
    if code_block_dict["parent_folder_id"] != "-1":
        update_operation ={"$push": {"child_code_blocks": str(response.inserted_id)}}
        filter_query = {"_id":  ObjectId(code_block_dict["parent_folder_id"])}
        folders_db.update_one(filter_query, update_operation)

def get_code_block_from_db(code_block_id: str):
    """Get code block from it's _id in code_blocks collection

    Args:
        code_block_id (str): _description_

    Returns:
        _type_: _description_
    """
    code_block = code_blocks_db.find_one({"_id": ObjectId(code_block_id)})

    if code_block is not None:
        code_block["_id"] = str(code_block["_id"])

    return code_block


def search_code_block_from_db(code_block_name: str, user_id: str):
    """Search code block by it's name and user_id combine 

    Args:
        code_block_name (str): _description_
        user_id (str): _description_

    Returns:
        _type_: _description_
    """

    pipeline = [{"$match": {"user_id": user_id, "code_block_name": code_block_name}}]
    matching_folders = list(code_blocks_db.aggregate(pipeline))

    for code_block in matching_folders:
        code_block["_id"] = str(code_block["_id"])

    return matching_folders


def update_code_block_in_db(code_block_id: str, code_block: CodeBlock):
    """Update code block

    Args:
        code_block_id (str): _description_
        code_block (CodeBlock): _description_

    Raises:
        HTTPException: _description_
    """

    if get_code_block_from_db(code_block_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="code block does not exist"
        )

    code_block_dict = code_block.model_dump()
    code_block_dict["_id"] = ObjectId(code_block_id)

    filter_query = {"_id": ObjectId(code_block_id)}
    update_operation = {"$set": code_block_dict}
    code_blocks_db.update_one(filter_query, update_operation)


def delete_code_block_from_db(code_block_id: str):
    """Delete code block from code_blocks collection"""

    code_block = get_code_block_from_db(code_block_id)

    if code_block is not None:
        code_blocks_db.delete_one({"_id": ObjectId(code_block_id)})

        filter_query = {"_id": ObjectId(code_block["parent_folder_id"])}
        update_operation = {"$pull": {"child_code_blocks": code_block["_id"]}}
        folders_db.update_one(filter_query,update_operation)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="code block not found")


def delete_code_block_from_db_by_user_id(user_id: str):
    """Delete all the code blocks based on user id"""
    filter_query = {"user_id": user_id}
    code_blocks_db.delete_many(filter_query)
