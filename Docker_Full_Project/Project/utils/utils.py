from enum import Enum
from typing import List
from bson import ObjectId
from fastapi import WebSocket, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu

from ValidationStudioCloud.utils.exceptions import (
    ErrorCodes,
    ValidationStudioError,
)

ID_FIELD_LIST = []


def convert_str_id_to_object_id(base_model, filter_dict):
    """
    Method to convert str ObjectId to bson.ObjectId
    Using the model it will fetch the id_fields and checks
    If any of the id field available then will convert to objectid
    """
    id_fields = base_model.Config.id_fields
    id_fields.add("_id")
    for field in id_fields:
        if filter_dict.get(field):
            if isinstance(filter_dict[field], list):
                for ind, value in enumerate(filter_dict[field]):
                    filter_dict[field][ind] = ObjectId(filter_dict[field][ind])
            else:
                filter_dict[field] = ObjectId(filter_dict[field])
    return filter_dict


async def process_data(base_model, db_instance, data):
    """
    Function to do foreign key check
    :param base_model:
    :param db_instance:
    :param data:
    :return:dict
    """
    data = convert_str_id_to_object_id(base_model, data)
    foreign_key = base_model.Config.foreign_key
    for key, value in foreign_key.items():
        if data.get(key) is not None:
            filter_values = data[key]
            if not isinstance(data[key], list):
                filter_values = [data[key]]
            for filter_value in filter_values:
                await process_data_core(value, db_instance, filter_value)
    return data


async def process_data_core(value, db_instance, filter_value):
    read_data = await rcu.read_documents(
        db_instance[value[0]],
        {value[1]: filter_value},
        {},
    )
    if len(read_data) == 0:
        detail = f"Foreign key check failed. Provided {value[1]} is not present in {value[0]} "
        raise ValidationStudioError(
            ErrorCodes.DOCUMENT_NOT_FOUND,
            ("utils", "process_data"),
            detail=detail,
        )


async def soft_delete_pre_check(doc_id, data, db_instance, collection_name):
    """Function to check the mandatory fields is present while we soft delete"""
    # document check to ensure is_deleted is not already true
    is_deleted_field = await rcu.read_documents(
        db_instance[f"{collection_name}"],
        {"_id": ObjectId(doc_id)},
        {},
    )
    if not is_deleted_field:
        raise ValidationStudioError(
            error_code=ErrorCodes.DOCUMENT_NOT_FOUND,
            location=(f"{collection_name}", "update"),
            detail="No Document Found",
        )

    if data.get("is_deleted") and not data.get("deleted_by"):
        raise ValidationStudioError(
            error_code=ErrorCodes.MANDATORY_FIELD_MISSING,
            location=(f"{collection_name}", "update"),
            detail="You are trying to change is_deleted field to true, make sure deleted_by field too along with it",
        )

    if not data.get("is_deleted") and data.get("deleted_by"):
        raise ValidationStudioError(
            error_code=ErrorCodes.MANDATORY_FIELD_MISSING,
            location=(f"{collection_name}", "update"),
            detail="You are trying to update the deleted_by field, make sure is_deleted should be update to True",
        )

    return True


def convert_list_dicts_to_dict(args):
    """Convert list of dictionary to dictionary format"""

    return dict((x["name"], x["value"]) for x in args)


def convert_object_id_to_str_id(list_of_dict):
    """convert object_id to a string in a list of dictionaries. It is not applicable for embedded level"""

    for ele in list_of_dict:
        ele["_id"] = str(ele["_id"])

    return list_of_dict


