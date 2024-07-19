"""
    Module: instruments_category.py

    Author: Nashith vp

    Description: Model for roles

    License:

    Created on: 01/07/2024

"""

from typing import Optional, Union

from pydantic import BaseModel, Field
from datetime import datetime
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class InstrumentCategory(BaseModel):
    """Instrument category model"""

    id: PydanticObjectId = Field(default="", alias="_id")
    organisation_id: PydanticObjectId
    name: str
    created_by: Optional[Union[PydanticObjectId, None]] = None
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
                "id": "666b578aba5977cc5816b8b7",
                "organisation_id": "666b578aba5977cc5816b8b8",
                "name": "Test Engineer",
                "created_by": "666b578aba5977cc5816b8b8",
                "is_deleted": False,
                "deleted_by": "666b578aba5977cc5816b8b8",
            }
        }
        key_fields: set = {"name", "organisation_id"}
        id_fields: set = {"id", "organisation_id", "created_by", "deleted_by"}
        foreign_key = {
            "organisation_id": ("organisations", "_id"),
            "created_by": ("users", "_id"),
            "deleted_by": ("users", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
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
                    "id": "666b578aba5977cc5816b8b7",
                    "organisation_id": "666b578aba5977cc5816b8b8",
                    "name": "Test Engineer",
                    "created_by": "666b578aba5977cc5816b8b8",
                    "created_on": "datatime",
                    "last_updated": "datetime",
                    "is_deleted": False,
                    "deleted_by": "666b578aba5977cc5816b8b8",
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(alias="_id", default=1)
        organisation_id: Optional[int] = 1
        name: Optional[int] = 1
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
                    "id": 1,
                    "organisation_id": 1,
                    "name": 1,
                    "created_by": 1,
                    "created_on": 1,
                    "last_updated": 1,
                    "is_deleted": 1,
                    "deleted_by": 1,
                }
            }
