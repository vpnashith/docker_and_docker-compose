"""
    Module: platform_resources
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 06-26-2024
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class AvailablePermissions(str, Enum):
    """Enum class for available permissions"""

    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


class PlatformResources(BaseModel):
    """Platform Resources Model"""

    id: PydanticObjectId = Field("", alias="_id")
    name: str
    available_permissions: List[AvailablePermissions] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {"id": "", "name": "", "available_permissions": []}
        }
        key_fields: set = {"name"}
        id_fields = {"id"}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        name: Optional[str] = None
        available_permissions: Optional[List[AvailablePermissions]] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {"id": "", "name": "", "available_resources": []}
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(alias="_id", default=1)
        name: Optional[int] = 1
        available_permissions: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {"id": 1, "name": 1, "available_permissions": 1}
            }
