"""
    Module: instructions_responses
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
from ValidationStudioCloud.models.instructions_responses import Responses
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import process_data

router = APIRouter(
    prefix="/instructions/instruction_responses", tags=["instruction_responses"]
)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Responses.FilterBy],
    response_model_exclude_unset=True,
)
async def search_instruction_responses(
    filter_model: FilterModel[Responses.FilterBy, Responses.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search instruction_responses"""

    filter_by_dict = await process_data(
        Responses,
        db_instance,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_embedded_document(
        db_instance["instructions"],
        doc_id,
        "responses",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Responses])
async def create_instruction_responses(
    instruction_response: Responses,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in Instructions collection
    """

    instruction_responses = await process_data(
        Responses, db_instance, instruction_response.model_dump(exclude={"id"})
    )

    instruction_responses["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["instructions"],
        doc_id,
        "responses",
        instruction_responses,
        Responses.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Responses])
async def update_instruction_responses(
    instruction_responses: Responses.FilterBy,
    doc_id: str = Body(..., embed=True),
    response_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in instructions collection
    """

    instructions = await process_data(
        Responses,
        db_instance,
        instruction_responses.model_dump(exclude={"id"}, exclude_unset=True),
    )

    content = await rcu.update_embedded_document(
        db_instance["instructions"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(response_id)},
        "responses",
        instructions,
        Responses.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instruction_responses(
    doc_id: str = Body(..., embed=True),
    res_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in instructions collection
    """
    document_filter = {"_id": bson.ObjectId(doc_id)}
    content = await rcu.delete_embedded_document(
        db_instance["instructions"],
        document_filter,
        {"responses": {"_id": bson.ObjectId(res_id)}},
    )
    return content
