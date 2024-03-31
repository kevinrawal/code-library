import os
import sys
from bson.objectid import ObjectId

from fastapi import HTTPException, status

from config.database import folders_db
from models.folders import Folder
from services.code_block_services import delete_code_block_from_db

# THIS CODE IS TO ACCESS MODULES OUTSIDE ROUTE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def get_folder_from_db(folder_id: str):
    """Get folder from folders collection via id"""

    folder = folders_db.find_one({"_id": ObjectId(folder_id)})
    if folder is not None:
        folder["_id"] = str(folder["_id"])

    return folder


def search_folder_by_name_from_db(folder_name: str, user_id: str):
    """search folder by it's name"""

    pipeline = [{"$match": {"user_id": user_id, "folder_name": folder_name}}]
    matching_folders = list(folders_db.aggregate(pipeline))

    for folder in matching_folders:
        folder["_id"] = str(folder["_id"])

    return matching_folders


def add_folder_in_db(folder: Folder):
    """Add new folder in folders collection"""
    folder_dict = folder.model_dump()
    response = folders_db.insert_one(folder_dict)

    # if current folder is not a root folder add current foder in parent's child list 
    if folder_dict["parent_folder_id"] != "-1":
        update_operation = {"$push": {"child_folders": str(response.inserted_id)}}
        # Convert str to ObjectId otherwise it will not able to identify the parent folder
        filter_query = {"_id":  ObjectId(folder_dict["parent_folder_id"])}
        folders_db.update_one(filter_query, update_operation)

def update_folder_in_db(folder_id: str, folder: Folder):
    """Update Folder in foldes collection"""
    if get_folder_from_db(folder_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="folder not found"
        )

    folder_dict = folder.model_dump()
    folder_dict["_id"] = ObjectId(folder_id)

    filter_query = {"_id": ObjectId(folder_id)}
    update_operation = {"$set": folder_dict}
    folders_db.update_one(filter_query, update_operation)


def delete_folder_from_db(folder_id: str):
    """delete folder from folders collection"""
    folder = get_folder_from_db(folder_id)

    if folder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"folder with id {folder_id}, does not exist")

    if folder["parent_folder_id"] == "-1":
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can not delete root folder")

    #TODO - BELOW PROCESSES SHOULD RUN ASYNCROUNOUSLY 
     
    # delete all child code blocks
    for child_code_block_id in folder["child_code_blocks"]:
        delete_code_block_from_db(child_code_block_id)

    # delete all child folders
    for child_folder_id in folder["child_folders"]:
        delete_folder_from_db(child_folder_id)

    # delete self 
    folders_db.delete_one({"_id": ObjectId(folder_id)})

    # delete parent of current folder 
    filter_query = {"_id": ObjectId(folder["parent_folder_id"])}
    update_operation = {"$pull": {"child_folders": folder["_id"]}}
    folders_db.update_one(filter_query, update_operation)

def delete_folder_from_db_by_user_id(user_id: str):
    """Delete every folder by user if"""
    
    filter_query = {"user_id": user_id}
    folders_db.delete_many(filter_query)
