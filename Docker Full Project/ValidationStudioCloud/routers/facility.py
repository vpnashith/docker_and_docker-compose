"""
    Module: facility.py
    Author: Rithwik

    Description: Routers for the Facility class

    License:

    Created on: 09-07-2024

"""

import datetime
from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.facility import Facility
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data, soft_delete_pre_check
from ValidationStudioCloud.utils.exceptions import (
    MongoError,
    ValidationStudioError,
    ErrorCodes,
)

router = APIRouter(prefix="/facility", tags=["Facility"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Facility.FilterBy],
    response_model_exclude_unset=True,
)
async def search_facility(
        filter_model: FilterModel[Facility.FilterBy, Facility.Unset],
        db_instance=Depends(get_database),
):
    """
    API for search operation in facility collection
    """
    filter_by_dict = convert_str_id_to_object_id(
        Facility, filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True)
    )
    content = await rcu.read_documents(
        db_instance["facility"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Facility])
async def create_facility(facility: Facility, db_instance=Depends(get_database)):
    """
    API for create operation in Roles collection
    """

    try:
        data = await process_data(
            Facility, db_instance, facility.model_dump(exclude={"id", "deleted_by", "is_deleted"})
        )
    except MongoError as err:
        location = ("facility", "create")
        detail = "Foreign key check failed"
        raise ValidationStudioError(err.error_code, location, detail=detail) from err

    data["created_on"] = datetime.datetime.now()
    data["last_updated"] = datetime.datetime.now()

    content = await rcu.create_document(
        db_instance["facility"],
        data,
        Facility.Config.key_fields,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Facility)
async def update_facility(
        facility: Facility.FilterBy,
        doc_id: str = Body(..., embed=True),
        db_instance=Depends(get_database),
):
    """
    API for update operation in facility collection
    """
    read_data = await rcu.read_documents(
        db_instance["facility"],
        {"_id": bson.ObjectId(doc_id)},
        {},
    )
    try:
        data = await process_data(
            Facility, db_instance, facility.model_dump(exclude={"id", "created_on", "created_by"})
        )
    except MongoError as err:
        location = ("facility", "update")
        detail = "Foreign key check failed"
        raise ValidationStudioError(err.error_code, location, detail=detail) from err
    data["last_updated"] = datetime.datetime.now()
    data["created_on"] = read_data[0]["created_on"]
    data["created_by"] = read_data[0]["created_by"]

    # on update of is_deleted
    if "is_deleted" in data and "deleted_by" not in data:
        raise ValidationStudioError(
            ErrorCodes.MANDATORY_FIELD_MISSING,
            ("routers", "update"),
            detail="deleted_by field should be given when is_deleted is updating into true",
        )
    await soft_delete_pre_check(doc_id, facility, db_instance, "facility")
    content = await rcu.update_document(
        db_instance["facility"],
        bson.ObjectId(doc_id),
        data,
        facility.Config.key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_facility(
        doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in facility collection
    """
    content = await rcu.delete_document(
        db_instance["facility"], bson.ObjectId(doc_id)
    )

    return content
