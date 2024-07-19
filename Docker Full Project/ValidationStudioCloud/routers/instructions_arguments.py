"""
    Module: instructions_arguments
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 06-30-2024
"""

from typing import List, Optional

import bson
from fastapi import APIRouter, Body, Depends, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.instructions_arguments import Arguments
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import process_data

router = APIRouter(
    prefix="/instructions/instruction_arguments", tags=["instructions_arguments"]
)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Arguments.FilterBy],
    response_model_exclude_unset=True,
)
async def search_instruction_arguments(
    filter_model: FilterModel[Arguments.FilterBy, Arguments.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search instruction_arguments"""

    filter_by_dict = await process_data(
        Arguments,
        db_instance,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_embedded_document(
        db_instance["instructions"],
        doc_id,
        "arguments",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Arguments])
async def create_instruction_arguments(
    instruction_arguments: Arguments,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in instructions collection
    """

    instruction_argument = await process_data(
        Arguments,
        db_instance,
        instruction_arguments.model_dump(
            exclude_unset=True, by_alias=True, exclude={"id"}
        ),
    )

    instruction_argument["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["instructions"],
        doc_id,
        "arguments",
        instruction_argument,
        Arguments.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Arguments])
async def update_instruction_arguments(
    instruction_argument: Arguments.FilterBy,
    doc_id: str = Body(..., embed=True),
    arguments_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in instructions collection
    """

    instructions = await process_data(
        Arguments,
        db_instance,
        instruction_argument.model_dump(exclude={"id"}, exclude_unset=True),
    )

    content = await rcu.update_embedded_document(
        db_instance["instructions"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(arguments_id)},
        "arguments",
        instructions,
        Arguments.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instruction_arguments(
    doc_id: str = Body(..., embed=True),
    arg_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in instructions collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["instructions"],
        document_filter,
        {"arguments": {"_id": bson.ObjectId(arg_id)}},
    )
    return content
