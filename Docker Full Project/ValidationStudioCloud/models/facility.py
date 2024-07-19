"""
    Module: facility.py
    Author: Rithwik

    Description: Models for facility

    License:

    Created on: 08-07-2024

"""

from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Facility(BaseModel):
    id: PydanticObjectId = Field("", alias="_id")
    organisation_id: Union[None, PydanticObjectId] = Field(None, alias="org_id")
    name: str
    created_by: Optional[PydanticObjectId] = None
    created_on: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    last_updated: Optional[datetime] = None
    deleted_on: Optional[datetime] = None
    deleted_by: Optional[PydanticObjectId] = None

    class Config:
        """config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "",
                "organisation_id": "",
                "name": "",
                "created_by": "",
                "deleted_by": "",
            }
        }
        key_fields: set = {"name", "organisation_id"}
        id_fields = {"id", "organisation_id", "created_by", "deleted_by"}
        foreign_key = {
            "organisation_id": ("organisations", "_id"),
            "created_by": ("users", "_id"),
            "deleted_by": ("users", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
                        This is added because for query operation all the fields are optional while for
                        other operations, this is not the case"""
        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = Field(None, alias="org_id")
        name: Optional[str] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime] = None
        is_deleted: Optional[bool] = False
        last_updated: Optional[datetime] = None
        deleted_on: Optional[datetime] = None
        deleted_by: Optional[PydanticObjectId] = None

        class Config:
            """config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "",
                    "organisation_id": "",
                    "name": "",
                    "created_by": "",
                    "deleted_by": "",
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
                            This is added because for query operation all the fields are optional while for
                            other operations, this is not the case"""
        id: Optional[int] = Field(default=1, alias="_id")
        organisation_id: Optional[int] = Field(1, alias="org_id")
        name: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        is_deleted: Optional[int] = 1
        last_updated: Optional[int] = 1
        deleted_on: Optional[int] = 1
        deleted_by: Optional[int] = 1

        class Config:
            """config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": 1,
                    "organisation_id": 1,
                    "name": 1,
                    "created_by": 1,
                    "created_on": 1,
                    "is_deleted": 1,
                    "last_updated": 1,
                    "deleted_on": 1,
                    "deleted_by": 1,
                }
            }

                
