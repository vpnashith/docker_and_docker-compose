"""
    Module: channel_groups
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
from ValidationStudioCloud.models.sequence_channel_groups import ChannelGroups
from ValidationStudioCloud.utils.rest_utils import FilterModel

router = APIRouter(prefix="/sequences/channel_groups", tags=["channel_groups"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[ChannelGroups.FilterBy],
    response_model_exclude_unset=True,
)
async def search_channel_groups(
    filter_model: FilterModel[ChannelGroups.FilterBy, ChannelGroups.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search channel_groups"""

    filter_by_dict = filter_model.filter_by.model_dump(
        exclude_unset=True, by_alias=True
    )

    content = await rcu.read_embedded_document(
        db_instance["sequences"],
        doc_id,
        "channel_groups",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[ChannelGroups]
)
async def create_channel_groups(
    channel_groups: ChannelGroups,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in channel_groups collection
    """

    # channel_group = await process_data(
    #     ChannelGroups,
    #     db_instance,
    #     channel_groups.model_dump(
    #         exclude_unset=True, by_alias=True, exclude={"id"}
    #     ),
    # )

    channel_group = channel_groups.model_dump(exclude_unset=True, by_alias=True)
    channel_group["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["sequences"],
        doc_id,
        "channel_groups",
        channel_group,
        ChannelGroups.Config.key_fields,
        position,
    )

    return content


@router.put(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[ChannelGroups]
)
async def update_channel_groups(
    channel_groups: ChannelGroups.FilterBy,
    doc_id: str = Body(..., embed=True),
    channel_group_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in channel_groups collection
    """

    channel_group = channel_groups.model_dump(exclude={"id"}, exclude_unset=True)

    content = await rcu.update_embedded_document(
        db_instance["sequences"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(channel_group_id)},
        "channel_groups",
        channel_group,
        ChannelGroups.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel_groups(
    doc_id: str = Body(..., embed=True),
    channel_group_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in channel_groups collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["sequences"],
        document_filter,
        {"channel_groups": {"_id": bson.ObjectId(channel_group_id)}},
    )
    return content
