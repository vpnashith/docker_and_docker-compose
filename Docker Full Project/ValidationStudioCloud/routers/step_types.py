"""
    Module: step_types.py
    Author: Ajay

    Description:

    License:

    Created on: 11-07-2024

"""

from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.step_types import StepTypes
from ValidationStudioCloud.utils.exceptions import (
    MongoError,
    ValidationStudioError,
)
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data

router = APIRouter(prefix="/step_types", tags=["step_types"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[StepTypes.FilterBy],
    response_model_exclude_unset=True,
)
async def search_step_types(
    filter_model: FilterModel[StepTypes.FilterBy, StepTypes.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in step_types collection
    """
    content = await rcu.read_documents(
        db_instance["step_types"],
        convert_str_id_to_object_id(
            StepTypes,
            filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
        ),
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[StepTypes])
async def create_step_types(step_type: StepTypes, db_instance=Depends(get_database)):
    """
    API for create operation in step_types collection
    """
    try:
        data = await process_data(
            StepTypes, db_instance, step_type.model_dump(exclude={"id"})
        )
    except MongoError as err:
        location = ("step_type", "create")
        detail = "Foreign key check failed"
        raise ValidationStudioError(err.error_code, location, detail=detail) from err

    content = await rcu.create_document(
        db_instance["step_types"],
        data,
        step_type.Config.key_fields,
    )
    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=StepTypes)
async def update_step_types(
    step_type: StepTypes,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in step_types collection
    """

    try:
        data = await process_data(
            StepTypes, db_instance, step_type.model_dump(exclude={"id"})
        )
    except MongoError as err:
        location = ("step_type", "update")
        detail = "Foreign key check failed"
        raise ValidationStudioError(err.error_code, location, detail=detail) from err

    content = await rcu.update_document(
        db_instance["step_types"],
        bson.ObjectId(doc_id),
        data,
        StepTypes.Config.key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_step_types(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in step_types collection
    """
    content = await rcu.delete_document(
        db_instance["step_types"], bson.ObjectId(doc_id)
    )

    return content
