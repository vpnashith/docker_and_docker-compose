"""
    Module: userVariables
    Author: Neethukrishnan P

    Description:

    License:

    Created on: 07-10-2024
"""

from typing import List, Optional

import bson
from fastapi import APIRouter, Body, Depends, status

from ValidationStudioCloud.models.sequence_userVariables import UserVariables
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.utils.exceptions import MongoError, ValidationStudioError
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import process_data

router = APIRouter(
    prefix="/sequences/user_variables", tags=["sequences_user_variables"]
)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[UserVariables.FilterBy],
    response_model_exclude_unset=True,
)
async def search_user_variables(
    filter_model: FilterModel[UserVariables.FilterBy, UserVariables.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search operation in user variables"""

    filter_by_dict = await process_data(
        UserVariables,
        db_instance,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_embedded_document(
        db_instance["sequences"],
        doc_id,
        "userVariables",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )

    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[UserVariables]
)
async def create_user_variables(
    user_variables: UserVariables,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """API for create user variables"""
    try:
        user_variable = await process_data(
            UserVariables,
            db_instance,
            user_variables.model_dump(
                exclude_unset=True, by_alias=True, exclude={"id"}
            ),
        )
    except MongoError as e:
        raise ValidationStudioError(
            error_code=e.error_code,
            location=("sequences_user_variables", "create"),
            detail=e,
        )
    user_variable["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["sequences"],
        doc_id,
        "userVariables",
        user_variable,
        UserVariables.Config.key_fields,
        position,
    )

    return content


@router.put(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[UserVariables]
)
async def update_user_variables(
    user_variables: UserVariables.FilterBy,
    doc_id: str = Body(..., embed=True),
    user_variables_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for update operation in user_variables collection"""

    user_variable = await process_data(
        UserVariables,
        db_instance,
        user_variables.model_dump(exclude={"_id"}, exclude_unset=True),
    )

    content = await rcu.update_embedded_document(
        db_instance["sequences"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(user_variables_id)},
        "userVariables",
        user_variable,
        UserVariables.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_variables(
    doc_id: str = Body(..., embed=True),
    user_variables_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API fro delete operation in user variables"""

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["sequences"],
        document_filter,
        {"userVariables": {"_id": bson.ObjectId(user_variables_id)}},
    )
    return content
