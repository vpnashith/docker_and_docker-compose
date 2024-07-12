from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import Union

mongo_uri = "mongodb+srv://doadmin:<password>@vs-mongodb-001-c4099f9a.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=vs-mongodb-001"  # Update for cloud-based deployment

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["Demo_DB_TEST"]
collection = db["employee"] 

# Define a data model for items
class Item(BaseModel):
    name: str
    description: Union[str, None] = None

app = FastAPI()


@app.get("/items")
async def read_all_items():
    # Retrieve all items from the collection
    items = list(collection.find({},{"_id":0}))
    return items


@app.post("/items")
async def create_item(item: Item):
    # Insert the new item into the collection
    new_item_id = collection.insert_one(item.dict()).inserted_id
    return {"id": str(new_item_id), **item.dict()}  # Convert ObjectID to string


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    # Find the item with the specified ID
    item = collection.find_one({"_id": ObjectId(item_id)},{"_id":0})
    if item:
        return item
    else:
        return {"message": "Item not found"}


@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    # Update the item with the specified ID
    collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    return {"message": "Item updated successfully"}


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    # Delete the item with the specified ID
    collection.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Item deleted successfully"}


@app.post("/read_file")
async def read_file():
    with open("/ValidationStudioDocker/project1/mount_file_dir_1/file_1", "r") as file1, \
            open("/ValidationStudioDocker/project1/mount_file_dir_2/file_2", "r") as file2:
        return {"file_1": file1.read(), "file_2": file2.read()}
    # with open("file_demo", "r") as f:
    #     return {"f": f.read()}
