import os

import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv

load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS = 3000)
db = None

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db = client[os.getenv('MONGODB_DATABASE')]
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)