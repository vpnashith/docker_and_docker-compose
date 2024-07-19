"""
    Module: user.py
    Author: Radhika Krishnan

    Description: Routers for the Users class

    License:

    Created on: 26-06-2024

"""

import datetime
from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.users import User
from ValidationStudioCloud.routers.login import get_password_hash
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

router = APIRouter(prefix="/users", tags=["Users"])


async def check_user_is_org_owner(doc_id, db_instance):
    """Function to check if the requested role is having by any user"""
    user_doc = await rcu.read_documents(
        db_instance["users"], {"_id": bson.ObjectId(doc_id)}
    )

    user_email = user_doc[0].get("email")
    content = await rcu.read_documents(
        db_instance["organisations"], {"org_owner_email": user_email}
    )
    return True if content else False


async def check_user_is_owner(doc_id, db_instance):
    """Function to check if the requested role is having by any user"""

    user_doc = await rcu.read_documents(
        db_instance["users"], {"_id": bson.ObjectId(doc_id)}
    )

    role_id = user_doc[0].get("role_id")
    print(role_id)
    content = await rcu.read_documents(
        db_instance["roles"], {"_id": bson.ObjectId(role_id)}
    )
    print(content)
    role_name = content[0].get("name")

    return True if role_name == "Owner" else False


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[User.FilterBy],
    response_model_exclude_unset=True,
)
async def search_user(
    filter_model: FilterModel[User.FilterBy, User.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in users collection
    """
    content = await rcu.read_documents(
        db_instance["users"],
        convert_str_id_to_object_id(
            User, filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True)
        ),
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[User])
async def create_user(user: User, db_instance=Depends(get_database)):
    """
    API for create operation in users collection
    """
    user = await process_data(
        User,
        db_instance,
        user.model_dump(exclude={"id", "is_deleted"}),
    )

    if "favourite_project" in user and user.get("favourite_project") is not None:
        if len(user["favourite_project"]) > 5:
            return JSONResponse(
                content="Favourite Projects Accepts only 5 Projects, so It Exceeds The Max Limit",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    user["last_updated"] = datetime.datetime.now()
    user["is_deleted"] = False
    if user["password"] is not None:
        user["password"] = get_password_hash(password=user["password"])
    else:
        raise ValidationStudioError(
            ErrorCodes.MANDATORY_FIELD_MISSING,
            ("routers", "create"),
            detail="Create cant proceed without password",
        )
    content = await rcu.create_document(
        db_instance["users"], user, User.Config.key_fields
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def update_user(
    user: User.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in users collection
    """
    user = await process_data(
        User,
        db_instance,
        user.model_dump(exclude={"id"}, exclude_unset=True, by_alias=True),
    )
    if await check_user_is_owner(doc_id, db_instance) and await check_user_is_org_owner(
        doc_id, db_instance
    ):
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_IN_USE,
            location=("users", "update"),
            detail="Can't update the user, the user is both an owner and an org owner",
        )

    if user.get("favourite_project"):
        if len(user.get("favourite_project")) > 5:
            return JSONResponse(
                content="Favourite Projects Accepts only 5 Projects, so It Exceeds The Max Limit",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    user["last_updated"] = datetime.datetime.now()
    await soft_delete_pre_check(doc_id, user, db_instance, "users")
    if user.get("password"):
        user["password"] = get_password_hash(password=user["password"])

    content = await rcu.update_document(
        db_instance["users"], bson.ObjectId(doc_id), user, User.Config.key_fields
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in users collection
    """
    if await check_user_is_org_owner(doc_id, db_instance):
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_IN_USE,
            location=("users", "delete"),
            detail="Can't delete the user, The user is a org_owner",
        )

    content = await rcu.delete_document(db_instance["users"], bson.ObjectId(doc_id))

    return content
