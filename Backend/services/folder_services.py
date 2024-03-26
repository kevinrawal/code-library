import os
import sys
from bson.objectid import ObjectId

from fastapi import HTTPException, status
from config.database import folders_db
from models.folders import Folder

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
    folders_db.insert_one(folder_dict)


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
    folders_db.delete_one({"_id": ObjectId(folder_id)})
    # TODO - delete all it's child folder and code blocks


def delete_folder_from_db_by_id(user_id: str):
    """Delete every folder by user if"""
    filter_query = {"user_id": user_id}
    folders_db.delete_many(filter_query)
