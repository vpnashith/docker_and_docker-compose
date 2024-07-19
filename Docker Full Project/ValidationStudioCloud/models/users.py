"""
    Module: user.py
    Author: Radhika Krishnan

    Description: Models for users

    License:

    Created on: 26-06-2024

"""

from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class User(BaseModel):
    """User model"""

    id: PydanticObjectId = Field("", alias="_id")
    organisation_id: Union[None, PydanticObjectId] = None
    role_id: Union[None, PydanticObjectId] = None
    first_name: str
    last_name: str
    email: str
    password: str = None
    is_active: Optional[bool] = Field(False)
    is_deleted: Optional[bool] = False
    last_updated: Optional[datetime] = None
    default_project: Optional[PydanticObjectId] = None
    favourite_project: Optional[List[PydanticObjectId]] = None

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "667b9ee51bba59b25c43c652",
                "organisation_id": "667b9efe1bba59b25c43c653",
                "role_id": "667b9f141bba59b25c43c654",
                "first_name": "User",
                "last_name": "Name",
                "email": "username@gmail.com",
                "password": "user@123",
                "is_deleted": False,
                "default_project": "667d61068174e7aca658fec2",
                "favourite_project": ["667d61068174e7aca658fec2"],
            }
        }
        key_fields: set = {"first_name", "last_name", "email"}
        id_fields: set = {
            "id",
            "organisation_id",
            "role_id",
            "default_project",
            "favourite_project",
        }
        foreign_key = {
            "organisation_id": ("organisations", "_id"),
            "role_id": ("roles", "_id"),
            "default_project": ("projects", "_id"),
            "favourite_project": ("projects", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = Field(
            None, alias="organisation_id"
        )
        role_id: Optional[PydanticObjectId] = Field(None, alias="role_id")
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        email: Optional[str] = None
        password: Optional[str] = None
        is_active: Optional[bool] = None
        is_deleted: Optional[bool] = None
        last_updated: Optional[datetime] = None
        default_project: Optional[PydanticObjectId] = None
        favourite_project: Optional[List[PydanticObjectId]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "667b9ee51bba59b25c43c652",
                    "organisation_id": "667b9efe1bba59b25c43c653",
                    "role_id": "667b9f141bba59b25c43c654",
                    "first_name": "User",
                    "last_name": "Name",
                    "email": "username@gmail.com",
                    "password": "user@123",
                    "is_active": False,
                    "is_deleted": False,
                    "last_updated": None,
                    "default_project": "667d61068174e7aca658fec2",
                    "favourite_project": ["667d61068174e7aca658fec2"],
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(alias="_id", default=1)
        organisation_id: Optional[int] = 1
        role_id: Optional[int] = 1
        first_name: Optional[int] = 1
        last_name: Optional[int] = 1
        email: Optional[int] = 1
        password: Optional[int] = 1
        is_active: Optional[int] = 1
        is_deleted: Optional[int] = 1
        last_updated: Optional[int] = 1
        default_project: Optional[int] = 1
        favourite_project: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": 1,
                    "organisation_id": 1,
                    "role_id": 1,
                    "first_name": 1,
                    "last_name": 1,
                    "email": 1,
                    "password": 1,
                    "is_active": 1,
                    "is_deleted": 1,
                    "last_updated": 1,
                    "default_project": 1,
                    "favourite_project": 1,
                }
            }
