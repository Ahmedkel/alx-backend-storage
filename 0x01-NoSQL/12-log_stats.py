#!/usr/bin/env python3
"""this module contains the function log_stats"""
from pymongo import MongoClient


def print_stats(mongo_collection):
    """print some stats about Nginx logs stored in MongoDB"""
    total_logs = mongo_collection.count_documents({})
    print(f'{total_logs} logs')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_check_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
    

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx
    print_stats(collection)