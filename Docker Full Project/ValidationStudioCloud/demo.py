# """
#     Module:
#
#     Author: Nashith vp
#
#     Description:
#
#     License:
#
#     Created on:
#
# """
# import uvicorn
# # from pydantic import BaseModel
# # from datetime import datetime
# #
# #
# # class Demo(BaseModel):
# #     date: datetime
# from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
#
# """
#     Module:
#
#     Author: Nashith vp
#
#     Description:
#
#     License:
#
#     Created on:
#
# """
#
# # print("".join("hello world"))
#
# # d = {}
# # print(d.get("hi"))
# #
# # if not d.get("hi"):
# #     print("Hyt")
#
# from fastapi import FastAPI, Body
# from pydantic import BaseModel
# from pymongo import MongoClient
# from bson import ObjectId
#
# # Replace with your MongoDB connection string (URI)
# mongo_uri = "mongodb+srv://nashith:nashid007@cluster0.apd7a1d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Update for cloud-based deployment
#
# # Connect to MongoDB
# client = MongoClient(mongo_uri)
# db = client["your_database_name"]
# collection = db["your_collection_name"]  # Replace with your collection name
#
# # Define a data model for items
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#
# app = FastAPI()
#
#
# @app.get("/items")
# async def read_all_items():
#     # Retrieve all items from the collection
#     items = list(collection.find({}))
#     return items
#
#
# @app.post("/items")
# async def create_item(item: Item):
#     # Insert the new item into the collection
#     new_item_id = collection.insert_one(item.dict()).inserted_id
#     return {"id": str(new_item_id), **item.dict()}  # Convert ObjectID to string
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     # Find the item with the specified ID
#     item = collection.find_one({"_id": ObjectId(item_id)})
#     if item:
#         return item
#     else:
#         return {"message": "Item not found"}
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: str, item: Item):
#     # Update the item with the specified ID
#     collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
#     return {"message": "Item updated successfully"}
#
#
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: str):
#     # Delete the item with the specified ID
#     collection.delete_one({"_id": ObjectId(item_id)})
#     return {"message": "Item deleted successfully"}
#
#
# if __name__ == "__main__":
#     uvicorn.run(
#         app,
#         host="127.0.0.1",
#         reload=False,
#         port=8000
#     )
#
# d = {"a":1}
# d["b"] = 2
# print(d)
import jwt


# class Demo:
#     var = 10
#
#     def fun(self):
#         print(Demo.var)
#
# obj = Demo()
# obj.fun()

# from pathlib import Path
# from pydantic import BaseModel
#
#
# class MyModel(BaseModel):
#     path: Path
#     description: str
#
#
# # Example usage
# data = {"path": "/home/user/data", "description": "This is a text file"}
# model = MyModel(**data)
# print(f"Path: {model.path}")
# print(f"Description: {model.description}")

# def get_check_roles(required_permission):  ===> ("projects:read", "users:read")
#     payload = jwt.decode(token:str)
#     given_permission = payload["roles_permissions"]   ===> [{"projects":["write","update"]},{"usrers": ["update", "read"]},{"instructions":["execute"]}]
#
#     def check_role(given_permission):
#         for permission in required_permission:
#             for ele in given_permission:
#                 if ele.get(permission.split(':')[0]):
#                     if permission.split(":")[1] in ele.get(permission.split(':')[0]):
#                         return True
#                     else:
#                         raise  ValidationError()
#
#
#         pass
#
#     return check_role(given_permission)

# def fun(n):
#     n2 = 10
#     def fun2(n2):
#         print(n2)
#
#     return fun2(n2)
#
# fun(1)
