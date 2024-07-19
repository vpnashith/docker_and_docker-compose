"""
    Module: resources
    Author: Ajay

    Description:

    License:

    Created on: 11-07-2024
"""

from typing import List, Optional

import bson
from fastapi import APIRouter, Body, Depends, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.sequence_resources import Resources
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data

router = APIRouter(prefix="/sequences/resources", tags=["resources"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Resources.FilterBy],
    response_model_exclude_unset=True,
)
async def search_resources(
    filter_model: FilterModel[Resources.FilterBy, Resources.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search resources"""

    filter_by_dict = convert_str_id_to_object_id(
        Resources, filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True)
    )

    content = await rcu.read_embedded_document(
        db_instance["sequences"],
        doc_id,
        "resources",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Resources])
async def create_resources(
    resource: Resources,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in resource collection
    """

    resource_data = await process_data(
        Resources, db_instance, resource.model_dump(exclude={"id"}, by_alias=True)
    )

    resource_data["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["sequences"],
        doc_id,
        "resources",
        resource_data,
        Resources.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Resources])
async def update_resources(
    resource: Resources.FilterBy,
    doc_id: str = Body(..., embed=True),
    resource_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in resource collection
    """

    resource_data = await process_data(
        Resources,
        db_instance,
        resource.model_dump(exclude={"id"}, exclude_unset=True, by_alias=True),
    )

    content = await rcu.update_embedded_document(
        db_instance["sequences"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(resource_id)},
        "resources",
        resource_data,
        Resources.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resources(
    doc_id: str = Body(..., embed=True),
    resource_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in channels collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["sequences"],
        document_filter,
        {"resources": {"_id": bson.ObjectId(resource_id)}},
    )
    return content
