"""
    Module: organisations.py
    Author: Rahul George

    Description:
        NB: We will identify the user logged in via Appsmith(Frontend) and store the username in the created_by field.
        It is applicable Only for Organisation. So, we can avoid the circular dependency with user collection

    License:

    Created on: 13-06-2024

"""

from datetime import datetime
from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.organisations import Organisation
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Organisation.FilterBy],
    response_model_exclude_unset=True,
)
async def search_organisation(
    filter_model: FilterModel[Organisation.FilterBy, Organisation.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in organisation collection
    """

    filter_by_dict = convert_str_id_to_object_id(
        Organisation,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )
    content = await rcu.read_documents(
        db_instance["organisations"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[Organisation]
)
async def create_organisation(
    organisation: Organisation, db_instance=Depends(get_database)
):
    """
    API for create operation in organisation collection
    """
    organisation = convert_str_id_to_object_id(
        Organisation,
        organisation.model_dump(exclude={"id", "created_on", "last_updated"}),
    )
    organisation["created_on"] = datetime.now()
    organisation["last_updated"] = datetime.now()
    content = await rcu.create_document(
        db_instance["organisations"], organisation, Organisation.Config.key_fields
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Organisation)
async def update_organisation(
    organisation: Organisation.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in organisation collection
    """
    organisation = convert_str_id_to_object_id(
        Organisation,
        organisation.model_dump(
            exclude={"id", "created_on", "last_updated"}, exclude_unset=True
        ),
    )
    organisation["last_updated"] = datetime.now()
    content = await rcu.update_document(
        db_instance["organisations"],
        bson.ObjectId(doc_id),
        organisation,
        Organisation.Config.key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organisation(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in device collection
    """
    content = await rcu.delete_document(
        db_instance["organisations"], bson.ObjectId(doc_id)
    )

    return content
