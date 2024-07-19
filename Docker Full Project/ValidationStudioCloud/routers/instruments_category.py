"""
    Module: instruments_category.py

    Author: Nashith vp

    Description:

    License:

    Created on: 01/07/2024

"""

from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status
from datetime import datetime

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.instruments_category import InstrumentCategory
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import (
    convert_str_id_to_object_id,
    process_data,
    soft_delete_pre_check,
)
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    ErrorCodes,
)

router = APIRouter(prefix="/instruments_category", tags=["instruments category"])


async def check_instrument_with_the_category_exist(db_instance, instrument_category_id):
    """Function to check if the requested instrument_category is having by any instrument"""
    content = await rcu.read_documents(
        db_instance["instruments"],
        {"instrument_category": bson.ObjectId(instrument_category_id)},
    )
    return True if content else False


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[InstrumentCategory.FilterBy],
    response_model_exclude_unset=True,
)
async def search_instruments_category(
    filter_model: FilterModel[InstrumentCategory.FilterBy, InstrumentCategory.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in instruments_category collection
    """

    filter_by_dict = convert_str_id_to_object_id(
        InstrumentCategory,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_documents(
        db_instance["instruments_category"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[InstrumentCategory]
)
async def create_instruments_category(
    instrument_category: InstrumentCategory, db_instance=Depends(get_database)
):
    """
    API for create operation in instruments_category collection
    """

    instrument_category = await process_data(
        InstrumentCategory,
        db_instance,
        instrument_category.model_dump(exclude={"id", "created_on", "last_updated"}),
    )

    instrument_category["created_on"] = datetime.now()
    instrument_category["last_updated"] = datetime.now()
    content = await rcu.create_document(
        db_instance["instruments_category"],
        instrument_category,
        InstrumentCategory.Config.key_fields,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=InstrumentCategory)
async def update_instruments_category(
    instrument_category: InstrumentCategory.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in instruments_category collection
    """

    instrument_category = await process_data(
        InstrumentCategory,
        db_instance,
        instrument_category.model_dump(
            exclude={"id", "created_on", "last_updated"}, exclude_unset=True
        ),
    )

    # function to check both is_deleted anf deleted_by field present in soft delete
    if await soft_delete_pre_check(
        doc_id, instrument_category, db_instance, "instruments_category"
    ):
        instrument_category["last_updated"] = datetime.now()
        content = await rcu.update_document(
            db_instance["instruments_category"],
            bson.ObjectId(doc_id),
            instrument_category,
            InstrumentCategory.Config.key_fields,
        )
        return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instruments_category(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in instruments_category collection
    """
    # Restricting the deletion if instrument with this instruments_category exists
    if await check_instrument_with_the_category_exist(db_instance, doc_id):
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_IN_USE,
            location=("instruments_category", "delete"),
            detail="Can't delete the instrument category, There exist instrument with this category",
        )

    content = await rcu.delete_document(
        db_instance["instruments_category"], bson.ObjectId(doc_id)
    )
    return content
