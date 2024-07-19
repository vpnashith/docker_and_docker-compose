"""
    Module: roles.py

    Author: Nashith vp

    Description: Model for roles

    License:

    Created on: 26-06-2024

"""

from typing import List, Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.models.roles_permissions import RolesPermissions
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Roles(BaseModel):
    """Roles model"""

    id: PydanticObjectId = Field(default="", alias="_id")
    organisation_id: PydanticObjectId
    name: str
    permissions: List[RolesPermissions] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "666b578aba5977cc5816b8b7",
                "organisation_id": "666b578aba5977cc5816b8b8",
                "name": "Test Engineer",
                "permissions": [],
            }
        }
        key_fields: set = {"name", "organisation_id"}
        id_fields: set = {"id", "organisation_id"}
        foreign_key = {"organisation_id": ("organisations", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
        permissions: Optional[List[RolesPermissions]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "666b578aba5977cc5816b8b7",
                    "organisation_id": "666b578aba5977cc5816b8b8",
                    "name": "Test Engineer",
                    "permissions": [],
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(alias="_id", default=1)
        organisation_id: Optional[int] = 1
        name: Optional[int] = 1
        permissions: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {"id": 1, "organisation_id": 1, "name": 1, "permissions": 1}
            }
