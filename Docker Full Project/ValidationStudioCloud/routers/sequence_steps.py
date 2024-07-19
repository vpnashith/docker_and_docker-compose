"""
    Module: steps
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
from ValidationStudioCloud.models.sequence_steps import Steps
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import process_data

router = APIRouter(prefix="/sequences/steps", tags=["steps"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Steps.FilterBy],
    response_model_exclude_unset=True,
)
async def search_steps(
    filter_model: FilterModel[Steps.FilterBy, Steps.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search steps"""

    filter_by_dict = await process_data(
        Steps,
        db_instance,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_embedded_document(
        db_instance["sequences"],
        doc_id,
        "steps",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Steps])
async def create_steps(
    steps: Steps,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in steps collection
    """

    step = await process_data(
        Steps,
        db_instance,
        steps.model_dump(exclude_unset=True, by_alias=True, exclude={"id"}),
    )

    step["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["sequences"],
        doc_id,
        "steps",
        step,
        Steps.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Steps])
async def update_steps(
    steps: Steps,
    doc_id: str = Body(..., embed=True),
    step_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in steps collection
    """

    step = await process_data(
        Steps,
        db_instance,
        steps.model_dump(exclude={"id"}, exclude_unset=True),
    )

    content = await rcu.update_embedded_document(
        db_instance["sequences"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(step_id)},
        "steps",
        step,
        Steps.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_steps(
    doc_id: str = Body(..., embed=True),
    step_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in steps collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["sequences"],
        document_filter,
        {"steps": {"_id": bson.ObjectId(step_id)}},
    )
    return content
