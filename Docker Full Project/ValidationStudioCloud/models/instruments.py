"""
    Module: instruments.py
    Author: Ajay

    Description:Model for instruments

    License:

    Created on: 26-06-2024

"""

import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.models.drivers import Drivers
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Instruments(BaseModel):
    """instrument model"""

    id: PydanticObjectId = Field("", alias="_id")
    organisation_id: Optional[PydanticObjectId] = None
    manufacturer: str
    model: str
    instrument_category: Optional[PydanticObjectId] = None
    created_by: PydanticObjectId
    created_on: Optional[datetime.datetime] = None
    last_updated: datetime.datetime = Field(datetime.datetime.now())
    is_deleted: Optional[bool] = False
    deleted_by: Optional[PydanticObjectId] = None
    drivers: Optional[List[Drivers]] = []
    channels: Optional[list] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}
        key_fields: set = {"model", "manufacturer"}
        id_fields = {
            "id",
            "organisation_id",
            "instrument_category",
            "created_by",
            "deleted_by",
        }
        foreign_key = {
            "organisation_id": ("organisations", "_id"),
            "instrument_category": ("instruments_category", "_id"),
            "created_by": ("users", "_id"),
            "deleted_by": ("users", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = None
        manufacturer: Optional[str] = None
        model: Optional[str] = None
        instrument_category: Optional[PydanticObjectId] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime.datetime] = None
        last_updated: Optional[datetime.datetime] = None
        is_deleted: Optional[bool] = None
        deleted_by: Optional[PydanticObjectId] = None
        drivers: Optional[List[Drivers]] = None
        channels: Optional[list] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {}

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(1, alias="_id")
        organisation_id: Optional[int] = 1
        manufacturer: Optional[int] = 1
        model: Optional[int] = 1
        instrument_category: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        last_updated: Optional[int] = 1
        is_deleted: Optional[int] = 1
        deleted_by: Optional[int] = 1
        drivers: Optional[int] = 1
        channels: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {}
