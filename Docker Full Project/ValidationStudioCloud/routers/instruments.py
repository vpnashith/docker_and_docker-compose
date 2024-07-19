"""
    Module: instruments.py
    Author: Ajay

    Description:

    License:

    Created on: 26-06-2024

"""

import datetime
from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.instruments import Instruments
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import (
    convert_str_id_to_object_id,
    process_data,
    soft_delete_pre_check,
)

router = APIRouter(prefix="/instruments", tags=["Instruments"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Instruments.FilterBy],
    response_model_exclude_unset=True,
)
async def search_instruments(
    filter_model: FilterModel[Instruments.FilterBy, Instruments.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in instruments collection
    """
    content = await rcu.read_documents(
        db_instance["instruments"],
        convert_str_id_to_object_id(
            Instruments,
            filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
        ),
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Instruments])
async def create_instruments(
    instruments: Instruments, db_instance=Depends(get_database)
):
    """
    API for create operation in instruments collection
    """

    data = await process_data(
        Instruments,
        db_instance,
        instruments.model_dump(exclude={"id", "deleted_by", "is_deleted"}),
    )

    data["created_on"] = datetime.datetime.now()
    data["last_updated"] = datetime.datetime.now()
    content = await rcu.create_document(
        db_instance["instruments"],
        data,
        Instruments.Config.key_fields,
    )
    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Instruments)
async def update_instruments(
    instruments: Instruments.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in instrument collection
    """

    instruments = await process_data(
        Instruments,
        db_instance,
        instruments.model_dump(
            exclude={"id", "created_on", "created_by"}, exclude_unset=True
        ),
    )

    instruments["last_updated"] = datetime.datetime.now()
    await soft_delete_pre_check(doc_id, instruments, db_instance, "instruments")

    content = await rcu.update_document(
        db_instance["instruments"],
        bson.ObjectId(doc_id),
        instruments,
        Instruments.Config.key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instruments(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in instrument collection
    """
    content = await rcu.delete_document(
        db_instance["instruments"], bson.ObjectId(doc_id)
    )

    return content
