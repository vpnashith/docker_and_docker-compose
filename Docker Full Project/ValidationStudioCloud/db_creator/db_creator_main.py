"""
    Module: db_creator main

    Created on: 24-07-2023

"""

# pylint:disable=R0914
from pymongo import MongoClient

from ValidationStudioCloud.db_creator import organisations


def db_setup(db_name):
    """Starting point of the script"""
    my_client = MongoClient("mongodb://localhost:27017/?uuidRepresentation=standard")

    my_db = my_client[db_name]

    if db_name == "validation_studio":
        return
    if db_name == "test_db":
        return

    organisations.create_organisations(my_db)


def main():
    """main method"""
    for instance in db_instances:
        db_setup(instance)


if __name__ == "__main__":
    db_instances = ["validation_studio_cloud", "test_cloud"]
    main()
else:
    db_instances = ["test_local"]
