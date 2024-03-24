import dotenv
import os

import pymongo
from pymongo.mongo_client import MongoClient

dotenv.load_dotenv()

password = os.environ["MONGODB_PASSWORD"]

url = f"mongodb+srv://kevinrawal30:{password}@codelibrary.zoiyv11.mongodb.net/?retryWrites=true&w=majority&appName=CodeLibrary"

# connect to MongoAtlas
client = MongoClient(url)
db = client.codelibrary_db

# print(client.codelibrary_db.list_collection_names())
user_db = db["users"]
code_blocks_db = db["code_blocks"]
folders_db = db["folders"]
## ********************************************************************************* ## 

# BELOW CODES ARE JUST NEED TO RUN ONCE, NOW THEY ARE NOT USEFUL BUT IT IS FOR LEARNING THAT HOW I USED IT 
# folders_db.create_index([("user_id", pymongo.ASCENDING), ("folder_name", pymongo.ASCENDING)])
# user_db.create_index([("email_id")],unique=True)
# code_blocks_db.create_index([("user_id", pymongo.ASCENDING), ("code_block_name", pymongo.ASCENDING)])