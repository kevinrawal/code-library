import os
import sys
import asyncio
from bson.objectid import ObjectId

from fastapi import HTTPException, status

from config.database import code_blocks_db, folders_db
from models.code_blocks import CodeBlock, UpdateCodeBlock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def add_code_block_in_db(code_block: CodeBlock):
    """Add new Code block in code_block collection
       it automatically assing new _id t this code block which is of ObjectId type
    Args:
        code_block (CodeBlock): _description_
    """

    # convert code block into dictionary and then add to the code_blocks_db collection
    code_block_dict = code_block.model_dump()
    response = await code_blocks_db.insert_one(code_block_dict)

    # add this code block id into it's parent child_code_blocks list
    if code_block_dict["parent_folder_id"] != "-1":
        update_operation = {"$push": {"child_code_blocks": str(response.inserted_id)}}
        filter_query = {"_id": ObjectId(code_block_dict["parent_folder_id"])}
        await folders_db.update_one(filter_query, update_operation)


async def get_code_block_from_db(code_block_id: str):
    """Get code block from it's _id in code_blocks collection

    Args:
        code_block_id (str): _description_

    Returns:
        _type_: _description_
    """
    code_block = await code_blocks_db.find_one({"_id": ObjectId(code_block_id)})

    if code_block is not None:
        code_block["_id"] = str(code_block["_id"])

    return code_block


async def search_code_block_from_db(code_block_name: str, user_id: str):
    """Search code block by it's name and user_id combine

    Args:
        code_block_name (str): _description_
        user_id (str): _description_

    Returns:
        _type_: _description_
    """

    pipeline = [{"$match": {"user_id": user_id, "code_block_name": code_block_name}}]
    cursor = code_blocks_db.aggregate(pipeline)

    matching_code_blocks = []

    async for code_block in cursor:
        code_block["_id"] = str(code_block["_id"])
        matching_code_blocks.append(code_block)

    return matching_code_blocks


async def update_code_block_in_db(code_block: UpdateCodeBlock):
    """Update code block

    Args:
        code_block_id (str): _description_
        code_block (CodeBlock): _description_

    Raises:
        HTTPException: _description_
    """

    if await get_code_block_from_db(code_block.code_block_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="code block does not exist"
        )

    filter_query = {"_id": ObjectId(code_block.code_block_id)}
    update_operation = {
        "$set": {
            "code_block_name": code_block.code_block_name,
            "problem_statement": code_block.problem_statement,
            "approaches": code_block.approaches,
            "similar_questions": code_block.similar_questions,
        }
    }
    await code_blocks_db.update_one(filter_query, update_operation)


async def delete_code_block_from_db(code_block_id: str):
    """Delete code block from code_blocks collection"""

    code_block = await get_code_block_from_db(code_block_id)

    delete_tasks = []
    if code_block is not None:
        delete_tasks.append(code_blocks_db.delete_one({"_id": ObjectId(code_block_id)}))

        filter_query = {"_id": ObjectId(code_block["parent_folder_id"])}
        update_operation = {"$pull": {"child_code_blocks": code_block["_id"]}}
        delete_tasks.append(folders_db.update_one(filter_query, update_operation))

        await asyncio.gather(*delete_tasks)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="code block not found"
        )


async def delete_code_block_from_db_by_user_id(user_id: str):
    """Delete all the code blocks based on user id"""
    filter_query = {"user_id": user_id}
    await code_blocks_db.delete_many(filter_query)


async def delete_code_block_forcefully(code_block_id: str):
    """it delete code block by id and does not update parent,
    because it has gauranteed that parent will delete it self after this operation

    Args:
        code_block_id (str): _description_
    """
    await code_blocks_db.delete_one({"_id": ObjectId(code_block_id)})
