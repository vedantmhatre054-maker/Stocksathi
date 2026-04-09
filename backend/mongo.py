from dotenv import load_dotenv
import os
from pymongo import MongoClient

# 🔥 LOAD ENV FILE FIRST
load_dotenv()

# 🔥 GET URI FROM ENV
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["stocksathi"]

# Collections
users_collection = db["users"]
inventory_collection = db["inventory"]
transactions_collection = db["transactions"]