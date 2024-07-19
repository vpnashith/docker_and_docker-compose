"""
    Module: platform_resources
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 06-26-2024
"""

from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.platform_resources import PlatformResources
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id

router = APIRouter(prefix="/platform_resources", tags=["platform_resources"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[PlatformResources.FilterBy],
    response_model_exclude_unset=True,
)
async def search_platform_resources(
    filter_model: FilterModel[PlatformResources.FilterBy, PlatformResources.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in platform resources collection
    """
    filter_by_dict = convert_str_id_to_object_id(
        PlatformResources,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_documents(
        db_instance["platform_resources"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[PlatformResources]
)
async def create_platform_resources(
    platform_resources: PlatformResources, db_instance=Depends(get_database)
):
    """
    API for create operation in platform_resources collection
    """
    content = await rcu.create_document(
        db_instance["platform_resources"],
        platform_resources.model_dump(exclude={"id"}),
        platform_resources.Config.key_fields,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=PlatformResources)
async def update_platform_resources(
    platform_resources: PlatformResources.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in platform_resources collection
    """

    content = await rcu.update_document(
        db_instance["platform_resources"],
        bson.ObjectId(doc_id),
        platform_resources.model_dump(exclude={"id"}, exclude_unset=True),
        PlatformResources.Config.key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_platform_resources(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in platform_resources collection
    """
    content = await rcu.delete_document(
        db_instance["platform_resources"], bson.ObjectId(doc_id)
    )

    return content
