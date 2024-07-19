"""
    Module: roles.py

    Author: Nashith vp

    Description: route for roles

    License:

    Created on: 26-06-2024

"""

from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.roles import Roles
from ValidationStudioCloud.models.users import User
from ValidationStudioCloud.routers.user import create_user
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    ErrorCodes,
)

router = APIRouter(prefix="/roles", tags=["roles"])


async def check_user_having_the_role(role_doc_id, db_instance):
    """Function to check if the requested role is having by any user"""
    content = await rcu.read_documents(
        db_instance["users"], {"role_id": bson.ObjectId(role_doc_id)}
    )
    return True if content else False


async def check_role_is_owner(role_doc_id, db_instance):
    """Function to check if the requested role is having by any user"""
    content = await rcu.read_documents(
        db_instance["roles"], {"_id": bson.ObjectId(role_doc_id)}
    )
    role_name = content[0].get("name")
    return True if role_name == "Owner" else False


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Roles.FilterBy],
    response_model_exclude_unset=True,
)
async def search_roles(
    filter_model: FilterModel[Roles.FilterBy, Roles.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in roles collection
    """

    filter_by_dict = convert_str_id_to_object_id(
        Roles, filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True)
    )

    content = await rcu.read_documents(
        db_instance["roles"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Roles])
async def create_roles(role: Roles, db_instance=Depends(get_database)):
    """
    API for create operation in Roles collection
    """

    role = await process_data(Roles, db_instance, role.model_dump(exclude={"id"}))

    content = await rcu.create_document(
        db_instance["roles"], role, Roles.Config.key_fields
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Roles)
async def update_roles(
    role: Roles.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in roles collection
    """
    if await check_role_is_owner(doc_id, db_instance):
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_IN_USE,
            location=("roles", "update"),
            detail="Can't update the role, The role is Owner",
        )
    role = await process_data(
        Roles, db_instance, role.model_dump(exclude={"id"}, exclude_unset=True)
    )

    content = await rcu.update_document(
        db_instance["roles"],
        bson.ObjectId(doc_id),
        role,
        Roles.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_roles(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in roles collection
    """
    # Restricting the deletion if user with this role exists
    if await check_user_having_the_role(doc_id, db_instance):
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_IN_USE,
            location=("roles", "delete"),
            detail="Can't delete the role, There exist one or more user with this role",
        )
    if await check_role_is_owner(doc_id, db_instance):
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_IN_USE,
            location=("roles", "delete"),
            detail="Can't delete the role, The role is Owner",
        )

    content = await rcu.delete_document(db_instance["roles"], bson.ObjectId(doc_id))
    return content


@router.post("/create_default_roles", status_code=status.HTTP_201_CREATED)
async def create_default_roles(
    first_name: str = Body(..., embed=True),
    last_name: str = Body(..., embed=True),
    org_id: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    user_role: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for creating default user roles for the organisation admin"""

    # read organisation doc
    org_data = await rcu.read_documents(
        db_instance["organisations"], {"_id": bson.ObjectId(org_id)}, {}
    )
    if not org_data:
        raise ValidationStudioError(
            ErrorCodes.DOCUMENT_NOT_FOUND,
            location=("routers", "roles", "create_default_roles"),
            detail="org_id not present",
        )

    # get platform_resources
    platform_resources = await rcu.read_documents(
        db_instance["platform_resources"], {"name": "organisations"}, {}
    )
    if not platform_resources:
        raise ValidationStudioError(
            ErrorCodes.DOCUMENT_NOT_FOUND,
            location=(
                "routers",
                "roles",
                "create_default_roles",
                "platform_resources_create",
            ),
            detail="platform_resources not found for this organisation",
        )

    # creating roles
    try:
        roles = await create_roles(
            Roles(
                organisation_id=bson.ObjectId(org_data[0]["_id"]),
                name=user_role,
                permissions=[
                    {
                        "platform_resource_id": bson.ObjectId(
                            platform_resources[0]["_id"]
                        ),
                        "given_permissions": platform_resources[0][
                            "available_permissions"
                        ],
                    }
                ],
            ),
            db_instance,
        )
    except Exception as e:
        raise ValidationStudioError(
            ErrorCodes.MODIFY_DOCUMENT_FAILED,
            location=("routers", "create_default_roles", "create_roles"),
            detail=e,
        )

    # create user
    try:
        user = await create_user(
            User(
                organisation_id=bson.ObjectId(org_data[0].get("_id")),
                role_id=bson.ObjectId(roles[0].get("_id")),
                first_name=first_name,
                last_name=last_name,
                email=org_data[0]["org_owner_email"],
                password=password,
            ),
            db_instance,
        )
    except Exception as e:
        raise ValidationStudioError(
            ErrorCodes.MODIFY_DOCUMENT_FAILED,
            location=("routers", "create_default_roles", "create_user"),
            detail=e,
        )

    user = jsonable_encoder(user, custom_encoder={bson.ObjectId: str})
    return user
