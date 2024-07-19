"""
    Module: userVariables
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-10-2024
"""

from typing import Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class UserVariables(BaseModel):
    """user variables class"""

    id: PydanticObjectId = Field(default="", alias="_id")
    name: str
    value: str
    data_transform_id: PydanticObjectId

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}

        key_fields: set = {"name"}
        id_fields: set = {"id", "data_transform_id"}
        foreign_key = {"data_transform_id": ("data_transforms", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        name: Optional[str] = None
        value: Optional[str] = None
        data_transform_id: Optional[PydanticObjectId] = None

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
        value: Optional[int] = 1
        data_transform_id: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {}
