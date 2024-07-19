"""
    Module: step_types.py
    Author: Ajay

    Description:Model for step_types

    License:

    Created on: 11-07-2024

"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class StepTypes(BaseModel):
    """step_type model"""

    id: PydanticObjectId = Field("", alias="_id")
    name: str
    step_schema: Dict[str, Any]
    class_name: str

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}
        key_fields: set = {"name"}
        id_fields = {"id"}
        foreign_key = {}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        name: Optional[str] = None
        step_schema: Optional[Dict[str, Any]] = None
        class_name: Optional[str] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_bss_name = True
            json_schema_extra = {}

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(1, alias="_id")
        name: Optional[int] = 1
        step_schema: Optional[int] = 1
        class_name: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {}
