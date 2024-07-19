"""
    Module: instructions
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 06-30-2024
"""

from datetime import datetime
from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.instructions import Instructions
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    MongoError,
)
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import (
    convert_str_id_to_object_id,
    process_data,
    soft_delete_pre_check,
)

router = APIRouter(prefix="/instructions", tags=["instructions"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Instructions.FilterBy],
    response_model_exclude_unset=True,
)
async def search_instructions(
    filter_model: FilterModel[Instructions.FilterBy, Instructions.Unset],
    db_instance=Depends(get_database),
):
    """API for search instructions"""

    filter_by_dict = convert_str_id_to_object_id(
        Instructions,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_documents(
        db_instance["instructions"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[Instructions]
)
async def create_instructions(
    instructions: Instructions, db_instance=Depends(get_database)
):
    """
    API for create operation in Instructions collection
    """
    try:
        instruction = await process_data(
            Instructions, db_instance, instructions.model_dump(exclude={"id"})
        )
    except MongoError as e:
        raise ValidationStudioError(
            error_code=e.error_code,
            location=("instruction", "create"),
            detail="Foreign key check failed",
        )

    instruction["created_on"], instruction["last_updated"] = (
        datetime.now(),
        datetime.now(),
    )

    content = await rcu.create_document(
        db_instance["instructions"], instruction, Instructions.Config.key_fields
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Instructions)
async def update_instructions(
    instruction: Instructions.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in instructions collection
    """

    instructions = await process_data(
        Instructions,
        db_instance,
        instruction.model_dump(exclude={"id"}, exclude_unset=True),
    )

    instructions["last_updated"] = datetime.now()
    await soft_delete_pre_check(doc_id, instructions, db_instance, "instructions")

    content = await rcu.update_document(
        db_instance["instructions"],
        bson.ObjectId(doc_id),
        instructions,
        Instructions.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instructions(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for soft delete operation for instructions
    """

    content = await rcu.delete_document(
        db_instance["instructions"], bson.ObjectId(doc_id)
    )

    return content
