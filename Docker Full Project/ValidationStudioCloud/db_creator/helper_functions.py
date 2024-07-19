"""
    Module: Helper methods

    Created on: 24-07-2023

"""
from typing import Tuple


from pymongo.database import Database


def insert_docs(my_db, collection_name, docs):
    """
        Generic method to perform insert queries
    :param my_db: Instance of mongoDB
    :param collection_name: Name of the Collection as a string
    :param docs: An iterable to insert. list of dicts
    :return: id of the inserted documents as a list.
    """
    collection = my_db[collection_name]
    result = collection.insert_many(docs)
    if len(result.inserted_ids) != len(docs):
        raise ValueError("Some of the inserts failed, Investigate!! ")
    return result.inserted_ids


def drop_collections(my_client: Database, collection_names: Tuple[str]) -> None:
    """
    Generic method to wipe one or more collection in DB
    :param my_client: Instance of MongoDB database
    :param collection_names: Tuple of collection names
    :return:
    """
    if collection_names:
        print(f"Before clean-up:{my_client.list_collection_names()}")
        for collection in my_client.list_collection_names():
            my_client.drop_collection(collection)
    print(f"After clean-up:{my_client.list_collection_names()}")

