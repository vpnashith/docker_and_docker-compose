"""
    Module: driver.py
    Author: Ajay

    Description:Model for drivers

    License:

    Created on: 26-06-2024

"""

from typing import Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Drivers(BaseModel):
    """Driver  model"""

    id: PydanticObjectId = Field(default="", alias="_id")
    driver_class: str
    builder_class: str
    destroyer_class: str
    driver_path: str
    builder_path: str
    destroyer_path: str

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}
        key_fields: set = {"driver_class"}
        id_fields = {
            "id",
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        driver_class: Optional[str] = None
        builder_class: Optional[str] = None
        destroyer_class: Optional[str] = None
        driver_path: Optional[str] = None
        builder_path: Optional[str] = None
        destroyer_path: Optional[str] = None

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
        driver_class: Optional[int] = 1
        builder_class: Optional[int] = 1
        destroyer_class: Optional[int] = 1
        driver_path: Optional[int] = 1
        builder_path: Optional[int] = 1
        destroyer_path: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {}
