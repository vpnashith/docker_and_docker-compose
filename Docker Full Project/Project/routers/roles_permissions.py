"""
    Module: roles_permissions.py

    Author: Nashith vp

    Description: router for roles permission embedded

    License:

    Created on: 26-06-2024

"""

from typing import List, Optional

import bson
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.roles_permissions import RolesPermissions
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    ErrorCodes,
)

router = APIRouter(prefix="/roles/permissions", tags=["roles_permissions"])


async def check_permissions_exist_in_platform(
    permission, platform_resource_id, db_instance
):
    """Function to check permissions exist in the platform"""
    try:
        content = await rcu.read_documents(
            db_instance["platform_resources"],
            {"_id": bson.ObjectId(platform_resource_id)},
        )
        available_permissions_in_platform = set(content[0]["available_permissions"])
    except IndexError:
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_NOT_FOUND,
            location=("roles_permissions", "create", "check_function"),
            detail="Platform does not exists. Give some valid platform_resource_id",
        )
    return (
        True if set(permission).issubset(available_permissions_in_platform) else False
    )


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[RolesPermissions.FilterBy],
    response_model_exclude_unset=True,
)
async def search_permissions(
    filter_model: FilterModel[RolesPermissions.FilterBy, RolesPermissions.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for search operation in permission: embedded field in roles collection
    """

    filter_by_dict = convert_str_id_to_object_id(
        RolesPermissions,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )
    content = await rcu.read_embedded_document(
        db_instance["roles"],
        doc_id,
        "permissions",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[RolesPermissions]
)
async def create_permissions(
    roles_permissions: RolesPermissions,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in permission: embedded field in roles collection
    """

    roles_permissions_model_dict = await process_data(
        RolesPermissions,
        db_instance,
        roles_permissions.model_dump(exclude_unset=True, by_alias=True, exclude={"id"}),
    )

    # Restricting the user to add permission which is not present in the corresponding platform
    if not await check_permissions_exist_in_platform(
        roles_permissions_model_dict.get("given_permissions"),
        roles_permissions_model_dict.get("platform_resource_id"),
        db_instance,
    ):
        return JSONResponse(
            content="One or more given permission(s) is not there for this platform",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    roles_permissions_model_dict["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["roles"],
        doc_id,
        "permissions",
        roles_permissions_model_dict,
        RolesPermissions.Config.key_fields,
        position,
    )

    return content


@router.put(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[RolesPermissions]
)
async def update_permissions(
    roles_permissions: RolesPermissions.FilterBy,
    doc_id: str = Body(..., embed=True),
    permissions_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in permission: embedded field in roles collection
    """
    key_fields = RolesPermissions.Config.key_fields

    roles_permissions_model_dict = await process_data(
        RolesPermissions,
        db_instance,
        roles_permissions.model_dump(exclude_unset=True, exclude={"id"}),
    )

    # Restricting the user to add permission which is not present in the corresponding platform
    if not await check_permissions_exist_in_platform(
        roles_permissions_model_dict.get("given_permissions"),
        roles_permissions_model_dict.get("platform_resource_id"),
        db_instance,
    ):
        return ValidationStudioError(
            error_code=ErrorCodes.UNHANDLED_ERROR,
            location=("roles_permission", "update"),
            detail="One or more given permission(s) is not there for this platform",
        )

    content = await rcu.update_embedded_document(
        db_instance["roles"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(permissions_id)},
        "permissions",
        roles_permissions_model_dict,
        key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permissions(
    doc_id: str = Body(..., embed=True),
    permissions_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in permission: embedded field in roles collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["roles"],
        document=document_filter,
        delete_condition={"permissions": {"_id": bson.ObjectId(permissions_id)}},
    )

    return content
