"""
    Module: stations_instruments.py
    Author: Radhika Krishnan

    Description: Models for stations instruments

    License:

    Created on: 05-07-2024

"""

from typing import Optional, List

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Configuration(BaseModel):
    name: str
    value: str


class Instruments(BaseModel):
    """class instruments"""

    id: PydanticObjectId = Field("", alias="_id")
    instrument_id: PydanticObjectId
    instrument_alias: Optional[str] = None
    configuration: List[Configuration] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "",
                "instrument_id": "",
                "instrument_alias": "",
                "configuration": [{"name": "", "value": ""}],
            }
        }
        key_fields: set = {"instrument_alias"}
        id_fields = {"id", "instrument_id"}
        foreign_key = {"instrument_id": ("instruments", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        instrument_id: Optional[PydanticObjectId] = None
        instrument_alias: Optional[str] = None
        Configuration: Optional[List[Configuration]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "",
                    "instrument_id": "",
                    "instrument_alias": "",
                    "configuration": [{"name": "", "value": ""}],
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        instrument_id: Optional[int] = 1
        instrument_alias: Optional[int] = 1
        Configuration: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": 1,
                    "instrument_id": 1,
                    "instrument_alias": 1,
                    "configuration": 1,
                }
            }
