"""
    Module: projects.py
    Author: Rithwik

    Description: Model for projects

    License:

    Created on: 28-06-2024

"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Project(BaseModel):
    """Project model"""

    id: PydanticObjectId = Field("", alias="_id")
    organisation_id: Optional[PydanticObjectId] = None
    name: str
    is_archived: Optional[bool] = False
    created_by: Optional[PydanticObjectId] = None
    created_on: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    updated_by: PydanticObjectId = None
    users: Optional[List[PydanticObjectId]] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "",
                "organisation_id": "",
                "name": "",
                "created_by": "",
                "updated_by": "",
                "users": [],
            }
        }
        key_fields: set = {"name", "organisation_id"}
        id_fields: set = {"id", "organisation_id", "created_by", "updated_by", "users"}
        foreign_key = {
            "organisation_id": ("organisations", "_id"),
            "created_by": ("users", "_id"),
            "updated by": ("users", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
        is_archived: Optional[bool] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime] = None
        last_updated: Optional[datetime] = None
        is_deleted: Optional[bool] = None
        updated_by: Optional[PydanticObjectId] = None
        users: Optional[List[PydanticObjectId]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "",
                    "organisation_id": "",
                    "name": "",
                    "created_by": "",
                    "updated_by": "",
                    "users": [],
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(alias="_id", default=1)
        organisation_id: Optional[int] = 1
        name: Optional[int] = 1
        is_archived: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        last_updated: Optional[int] = 1
        is_deleted: Optional[int] = 1
        updated_by: Optional[int] = 1
        users: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": 1,
                    "organisation_id": 1,
                    "name": 1,
                    "is_archived": 1,
                    "created_by": 1,
                    "created_on": 1,
                    "last_updated": 1,
                    "is_deleted": 1,
                    "updated_by": 1,
                    "users": 1,
                }
            }
