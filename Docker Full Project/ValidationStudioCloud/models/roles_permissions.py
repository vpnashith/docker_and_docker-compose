"""
    Module: roles_permissions.py

    Author: Nashith vp

    Description: Model for roles permission embedded

    License:

    Created on: 26-06-2024

"""

from typing import List, Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class RolesPermissions(BaseModel):
    """Roles Permissions model"""

    id: PydanticObjectId = Field(default="", alias="_id")
    platform_resource_id: PydanticObjectId
    given_permissions: List[str] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "666b578aba5977cc5816b8b7",
                "platform_resource_id": "667b9aaa238cd11e14ea6850",
                "given_permissions": [],
            }
        }
        key_fields: set = {"platform_resource_id"}
        id_fields: set = {"id", "platform_resource_id"}
        foreign_key = {"platform_resource_id": ("platform_resources", "_id")}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        platform_resource_id: Optional[PydanticObjectId] = None
        given_permissions: Optional[List[str]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "666b578aba5977cc5816b8b7",
                    "platform_resource_id": "667b9aaa238cd11e14ea6850",
                    "given_permissions": [],
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(default=1, alias="_id")
        platform_resource_id: Optional[int] = 1
        given_permissions: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {"_id": 1, "platform_resource_id": 1, "given_permissions": 1}
            }
