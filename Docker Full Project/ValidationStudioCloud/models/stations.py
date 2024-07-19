"""
    Module: stations.py
    Author: Radhika Krishnan

    Description: Models for stations

    License:

    Created on: 04-07-2024

"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId
from ValidationStudioCloud.models.stations_instruments import Instruments


class Stations(BaseModel):
    """Stations Model"""

    id: PydanticObjectId = Field("", alias="_id")
    organisation_id: PydanticObjectId
    facility_id: Optional[PydanticObjectId] = None
    name: str
    ip_address: Optional[str] = None
    created_by: Optional[PydanticObjectId] = None
    created_on: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    instruments: Optional[List[Instruments]] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "",
                "organisation_id": "",
                "facility_id": "",
                "name": "",
                "ip_address": "",
                "created_by": "",
                "is_deleted": False,
                "instruments": [],
            }
        }
        key_fields: set = {"name", "organisation_id"}
        id_fields: set = {"id", "organisation_id", "facility_id", "created_by"}
        foreign_key = {
            "organisation_id": ("organisations", "_id"),
            "facility_id": ("facility", "_id"),
            "created_by": ("users", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = None
        facility_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
        ip_address: Optional[str] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime] = None
        last_updated: Optional[datetime] = None
        is_deleted: Optional[bool] = False
        instruments: Optional[List[Instruments]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": "",
                    "organisation_id": "",
                    "facility_id": "",
                    "name": "",
                    "ip_address": "",
                    "created_by": "",
                    "created_on": "",
                    "last_updated": "",
                    "is_deleted": False,
                    "instruments": [],
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        organisation_id: Optional[int] = 1
        facility_id: Optional[int] = 1
        name: Optional[int] = 1
        ip_address: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        last_updated: Optional[int] = 1
        is_deleted: Optional[int] = 1
        instruments: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": 1,
                    "organisation_id": 1,
                    "facility_id": 1,
                    "name": 1,
                    "ip_address": 1,
                    "created_by": 1,
                    "created_on": 1,
                    "last_updated": 1,
                    "is_deleted": 1,
                    "instruments": 1,
                }
            }
