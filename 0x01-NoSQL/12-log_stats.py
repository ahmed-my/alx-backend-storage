#!/usr/bin/python3
"""
Python script that provides some stats about Nginx
"""


from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient()
db = client.logs
collection = db.nginx

# Count total logs
total_logs = collection.count_documents({})

print(f"{total_logs} logs")

# Count methods
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = {method: collection.count_documents({"method": method})
                 for method in methods}

print("Methods:")
for method, count in method_counts.items():
    print(f"    method {method}: {count}")

# Count status check
status_count = collection.count_documents({"method": "GET", "path": "/status"})

print(f"{status_count} status check")
