"""
    Module: instructions
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 06-28-2024
"""

from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, Field

from ValidationStudioCloud.models.instructions_arguments import Arguments
from ValidationStudioCloud.models.instructions_responses import Responses
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Instructions(BaseModel):
    """Instructions Model"""

    id: PydanticObjectId = Field("", alias="_id")
    instrument_id: PydanticObjectId = Field(..., alias="instrument_id")
    project_id: Optional[Union[PydanticObjectId, None]] = None
    name: str
    description: Optional[str] = None
    arguments: Optional[List[Arguments]] = []
    responses: Optional[List[Responses]] = []
    created_by: Optional[Union[PydanticObjectId, None]] = None
    created_on: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    is_deleted: bool = False
    deleted_on: Union[None, datetime] = None

    class Config:
        """config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "",
                "instrument_id": "",
                "project_id": "",
                "name": "",
                "description": "",
                "arguments": [],
                "responses": [],
                "created_by": "",
            }
        }
        key_fields: set = {"name", "instrument_id"}
        id_fields = {"id", "instrument_id", "project_id", "created_by"}
        foreign_key = {
            "created_by": ("users", "_id"),
            "project_id": ("projects", "_id"),
            "instrument_id": ("instruments", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        instrument_id: Optional[PydanticObjectId] = None
        project_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
        description: Optional[str] = None
        arguments: Optional[List[Arguments]] = None
        responses: Optional[List[Responses]] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime] = None
        last_updated: Optional[datetime] = None
        is_deleted: Optional[bool] = None
        deleted_on: Optional[datetime] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": "",
                    "instrument_id": "",
                    "project_id": "",
                    "name": "",
                    "description": "",
                    "arguments": [],
                    "responses": [],
                    "created_by": "",
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        instrument_id: Optional[int] = 1
        project_id: Optional[int] = 1
        name: Optional[int] = 1
        description: Optional[int] = 1
        arguments: Optional[int] = 1
        responses: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        last_updated: Optional[int] = 1
        is_deleted: Optional[int] = 1
        deleted_on: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "_id": 1,
                    "instrument_id": 1,
                    "project_id": 1,
                    "name": 1,
                    "description": 1,
                    "arguments": 1,
                    "responses": 1,
                    "created_by": 1,
                    "created_on": 1,
                    "last_updated": 1,
                    "is_deleted": 1,
                    "deleted_on": 1,
                }
            }
