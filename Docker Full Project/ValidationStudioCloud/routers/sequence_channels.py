"""
    Module: channels
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-11-2024
"""

from typing import List, Optional

import bson
from fastapi import APIRouter, Body, Depends, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.sequence_channels import Channels
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id

router = APIRouter(prefix="/sequences/channels", tags=["channels"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Channels.FilterBy],
    response_model_exclude_unset=True,
)
async def search_channels(
    filter_model: FilterModel[Channels.FilterBy, Channels.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search channels"""

    filter_by_dict = convert_str_id_to_object_id(
        Channels, filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True)
    )

    content = await rcu.read_embedded_document(
        db_instance["sequences"],
        doc_id,
        "channels",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Channels])
async def create_channels(
    channels: Channels,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in channels collection
    """

    channel = channels.model_dump(exclude_unset=True, by_alias=True)

    channel["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["sequences"],
        doc_id,
        "channels",
        channel,
        Channels.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Channels])
async def update_channels(
    channels: Channels.FilterBy,
    doc_id: str = Body(..., embed=True),
    channel_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in channels collection
    """

    channel = channels.model_dump(exclude={"id"}, exclude_unset=True)

    content = await rcu.update_embedded_document(
        db_instance["sequences"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(channel_id)},
        "channels",
        channel,
        Channels.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channels(
    doc_id: str = Body(..., embed=True),
    channel_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in channels collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["sequences"],
        document_filter,
        {"channels": {"_id": bson.ObjectId(channel_id)}},
    )
    return content
