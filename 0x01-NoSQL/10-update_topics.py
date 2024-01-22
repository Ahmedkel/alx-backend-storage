#!/usr/bin/env python3
"""this module contains the function update_topics"""


def update_topics(mongo_collection, name, topics):
    """this function updates a document based on name"""
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
