"""
    Module: data_transforms
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-03-2024
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class DataTransform(BaseModel):
    """DataTransforms model"""

    id: PydanticObjectId = Field(default="", alias="_id")
    project_id: PydanticObjectId
    name: str
    is_response_df: Optional[bool] = False
    description: Optional[str] = None
    file_path: Optional[str] = None
    created_by: PydanticObjectId
    created_on: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    deleted_by: Optional[PydanticObjectId] = None

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "",
                "project_id": "",
                "name": "",
                "is_response_df": False,
                "description": "",
                "file_path": "",
                "created_by": "",
                "is_deleted": False,
                "deleted_by": "",
            }
        }
        key_fields: set = {"name"}
        id_fields: set = {"id", "project_id", "created_by", "deleted_by"}
        foreign_key = {"project_id": ("projects", "_id"), "users": ("users", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        project_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
        is_response_df: Optional[bool] = None
        description: Optional[str] = None
        file_path: Optional[str] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime] = None
        last_updated: Optional[datetime] = None
        is_deleted: Optional[bool] = None
        deleted_by: Optional[PydanticObjectId] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "project_id": "",
                    "name": "",
                    "is_response_df": False,
                    "description": "",
                    "file_path": "",
                    "created_by": "",
                    "is_deleted": False,
                    "deleted_by": "",
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        project_id: Optional[int] = 1
        name: Optional[int] = 1
        is_response_df: Optional[int] = 1
        description: Optional[int] = 1
        file_path: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        last_updated: Optional[int] = 1
        is_deleted: Optional[int] = 1
        deleted_by: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": 1,
                    "project_id": 1,
                    "name": 1,
                    "is_response_df": 1,
                    "description": 1,
                    "file_path": 1,
                    "created_by": 1,
                    "created_on": 1,
                    "last_updated": 1,
                    "is_deleted": 1,
                    "deleted_by": 1,
                }
            }
