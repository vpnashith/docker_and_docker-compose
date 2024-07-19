"""
    Module: steps
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-10-2024
"""

from typing import Optional, Any, Dict

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Steps(BaseModel):
    """class for steps"""

    step_id: PydanticObjectId = Field(default="", alias="_id")
    name: str
    step_type_id: PydanticObjectId
    step_data: Dict[str, Any]

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}

        key_fields: set = {"name"}
        id_fields: set = {"id", "step_type_id"}
        foreign_key = {"step_types": ("step_types", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        step_id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        name: Optional[str] = None
        step_type_id: Optional[PydanticObjectId] = None
        step_data: Optional[Dict[str, Any]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {}

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        step_id: Optional[int] = Field(default=1, alias="_id")
        name: Optional[int] = None
        step_type_id: Optional[int] = 1
        step_data: Optional[int] = 1
