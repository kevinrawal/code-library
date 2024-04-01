"""Database config file"""

import os
import dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

password = os.environ["MONGODB_PASSWORD"]

uri = f"mongodb+srv://kevinrawal30:{password}@codelibrary.zoiyv11.mongodb.net/?retryWrites=true&w=majority&appName=CodeLibrary"

# connect to MongoAtlas
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
db = client.codelibrary_db

user_db = db["users"]
code_blocks_db = db["code_blocks"]
folders_db = db["folders"]

## *********BELOW CODE ARE TO SET UP PRIMARY AND COMPOUND KEYS********* ##

# add email id as primary index, _id is the default primary key and it will remain
# user_db.create_index([("email_id")],unique=True)

# creating compound indexes
# folders_db.create_index([("user_id", pymongo.ASCENDING), ("folder_name", pymongo.ASCENDING)])
# code_blocks_db.create_index([("user_id", pymongo.ASCENDING), ("code_block_name", pymongo.ASCENDING)])

# Below code Used to connect without motor 
# from pymongo.mongo_client import MongoClient
# client = MongoClient(url) change with original 