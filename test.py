import os

from dotenv import load_dotenv
from pymongo import MongoClient


# Load .env
load_dotenv()

# Get MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Select our database
db = client["Holiday_Planner"]

# Test connection
try:
    client.admin.command("ping")
    print("MongoDB connection successful! ✅")

    print("Database:", db.name)

except Exception as e:
    print("MongoDB connection failed! ❌")
    print("Error:", e)

finally:
    client.close()