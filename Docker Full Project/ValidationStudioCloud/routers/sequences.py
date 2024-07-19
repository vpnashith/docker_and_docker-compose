"""
    Module: sequences
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-11-2024
"""

from typing import List
from datetime import datetime
import bson

from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.sequences import Sequences
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    ErrorCodes,
    MongoError,
)

router = APIRouter(prefix="/sequences", tags=["sequences"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Sequences.FilterBy],
    response_model_exclude_unset=True,
)
async def search_sequences(
    filter_model: FilterModel[Sequences.FilterBy, Sequences.Unset],
    db_instance=Depends(get_database),
):
    """API for search operation sequences"""
    filter_by_dict = convert_str_id_to_object_id(
        Sequences,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_documents(
        db_instance["sequences"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Sequences])
async def create_sequences(sequences: Sequences, db_instance=Depends(get_database)):
    """API for create operation for sequences"""
    try:
        sequence = await process_data(
            Sequences, db_instance, sequences.model_dump(exclude={"id"})
        )
    except MongoError as e:
        raise ValidationStudioError(
            error_code=e.error_code,
            location=("sequences", "create"),
            detail=e,
        )

    sequence["created_on"] = datetime.now()
    sequence["last_updated"] = datetime.now()

    content = await rcu.create_document(
        db_instance["sequences"], sequence, Sequences.Config.key_fields
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Sequences)
async def update_sequences(
    sequences: Sequences.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for update operation in sequences"""

    sequence = await process_data(
        Sequences,
        db_instance,
        sequences.model_dump(exclude={"id"}, exclude_unset=True),
    )

    # on update of is_deleted
    if "is_deleted" in sequence and "deleted_by" not in sequence:
        raise ValidationStudioError(
            ErrorCodes.MANDATORY_FIELD_MISSING,
            ("routers", "update"),
            detail="deleted_by field should be given when is_deleted is updating into true",
        )

    sequence["last_updated"] = datetime.now()

    content = await rcu.update_document(
        db_instance["sequences"],
        bson.ObjectId(doc_id),
        sequence,
        Sequences.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sequences(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in sequences collection
    """

    content = await rcu.delete_document(db_instance["sequences"], bson.ObjectId(doc_id))
    return content
