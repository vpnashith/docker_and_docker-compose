"""
    Module: instructions_responses
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 06-30-2024
"""

from typing import Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Responses(BaseModel):
    """class responses"""

    id: PydanticObjectId = Field(default="", alias="_id")
    name: str
    byte_count: int
    data_transform_id: PydanticObjectId

    class Config:
        """config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "",
                "name": "",
                "byte_count": -1,
                "data_transform_id": "",
            }
        }
        key_fields: set = {"name", "data_transform_id"}
        id_fields = {"id", "data_transform_id"}
        foreign_key = {"data_transform_id": ("data_transforms", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        name: Optional[str] = None
        byte_count: Optional[int] = None
        data_transform_id: Optional[PydanticObjectId] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": "",
                    "name": "",
                    "byte_count": -1,
                    "data_transform_id": "",
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        name: Optional[int] = 1
        byte_count: Optional[int] = 1
        data_transform_id: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": 1,
                    "name": 1,
                    "byte_count": 1,
                    "data_transform_id": 1,
                }
            }
