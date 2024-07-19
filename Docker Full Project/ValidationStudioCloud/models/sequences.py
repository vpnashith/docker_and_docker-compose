"""
    Module: sequences
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-10-2024
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from ValidationStudioCloud.models.sequence_channel_groups import ChannelGroups
from ValidationStudioCloud.models.sequence_channels import Channels
from ValidationStudioCloud.models.sequence_resources import Resources
from ValidationStudioCloud.models.sequence_steps import Steps
from ValidationStudioCloud.models.sequence_userVariables import UserVariables
from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Sequences(BaseModel):
    """Class for sequences"""

    id: PydanticObjectId = Field(default="", alias="_id")
    organisation_id: PydanticObjectId
    project_id: PydanticObjectId
    name: str
    description: Optional[str] = None
    last_updated: Optional[datetime] = None
    created_by: PydanticObjectId = None
    created_on: Optional[datetime] = None
    resources: Optional[List[Resources]] = []
    channels: Optional[List[Channels]] = []
    channel_groups: Optional[List[ChannelGroups]] = []
    steps: Optional[List[Steps]] = []
    userVariables: Optional[List[UserVariables]] = []

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {}
        key_fields: set = {"name"}
        id_fields: set = {"id", "project_id", "created_by", "organisation_id"}
        foreign_key = {
            "project_id": ("projects", "_id"),
            "users": ("users", "_id"),
            "organisation_id": ("organisations", "_id"),
        }

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
        organisation_id: Optional[PydanticObjectId] = None
        project_id: Optional[PydanticObjectId] = None
        name: Optional[str] = None
        description: Optional[str] = None
        last_updated: Optional[datetime] = None
        created_by: Optional[PydanticObjectId] = None
        created_on: Optional[datetime] = None
        resources: Optional[List] = []
        channels: Optional[List[Channels]] = []
        channel_groups: Optional[List[ChannelGroups]] = []
        steps: Optional[List[Steps]] = []
        userVariables: Optional[List[UserVariables]] = []

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
        organisation_id: Optional[int] = 1
        project_id: Optional[int] = 1
        name: Optional[int] = 1
        description: Optional[int] = 1
        last_updated: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        resources: Optional[int] = 1
        channels: Optional[int] = 1
        channel_groups: Optional[int] = 1
        steps: Optional[int] = 1
        userVariables: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {}
