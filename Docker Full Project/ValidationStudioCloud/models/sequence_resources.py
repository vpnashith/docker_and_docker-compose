"""
    Module: resources
    Author: Ajay

    Description:

    License:

    Created on: 11-07-2024
"""

from typing import Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Resources(BaseModel):
    """class resources"""

    id: PydanticObjectId = Field(default="", alias="_id")
    name: str
    instrument_id: PydanticObjectId
    station_instrument_alias: Optional[str]

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}

        key_fields: set = {"name"}
        id_fields: set = {"id", "instrument_id"}
        foreign_key = {"instrument_id": ("instruments", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        name: Optional[str] = None
        instrument_id: Optional[PydanticObjectId] = None
        station_instrument_alias: Optional[str] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {}

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        name: Optional[int] = 1
        instrument_id: Optional[int] = 1
        station_instrument_alias: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {}
