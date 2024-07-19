"""
    Module: bson_object_id.py
    Author: Rahul George

    Description: To support the ObjectId type of BSON structure

    License:

    Created on: 01-11-2023

"""
# pylint:disable=E0611, C0103, W0108, C0116
from typing import Any, Union
from typing_extensions import Annotated
from bson import ObjectId
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PydanticObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]
