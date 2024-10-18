import pymongo
import random
import string
import time
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Insert dummy data into Cosmos DB (RU model).")
parser.add_argument("--cosmos_db_uri", type=str, required=True, help="Cosmos DB connection string")
args = parser.parse_args()

# Configuration settings
database_name = "sampleDatabase"
collection_name = "sampleCollection"
data_size_mb = 200  # Target data size in MB
document_size_kb = 20  # Approximate size of each document in KB

# Connect to Cosmos DB
client = pymongo.MongoClient(args.cosmos_db_uri)
db = client[database_name]
collection = db[collection_name]

# Function to generate a random string of specified size
def generate_random_string(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# Calculate the number of documents to insert
documents_count = (data_size_mb * 1024) // document_size_kb

# Document structure
def create_document():
    return {
        "name": generate_random_string(100),
        "description": generate_random_string(5000),
        "timestamp": time.time(),
        "metadata": {
            "category": generate_random_string(20),
            "tags": [generate_random_string(8) for _ in range(5)]
        }
    }

# Insert documents into the collection
for _ in range(documents_count):
    collection.insert_one(create_document())

print(f"Successfully inserted approximately {data_size_mb} MB of data into Cosmos DB.")
