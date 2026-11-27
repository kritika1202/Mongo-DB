import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017"),
    serverSelectionTimeoutMS=5000,
)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully")
except Exception as error:
    print("Connection failed:", error)
finally:
    client.close()