"""
    Module: tc_exceptions
    Author: Rahul George

    Description: Generic module encapsulating all the exceptions used in this project.

    License:

    Created on: 14-07-2022

"""

from enum import Enum
from typing import Tuple

from fastapi import HTTPException


class ErrorCodes(str, Enum):
    """Possible error codes generalized to enum to provide consistent response."""

    MANDATORY_FIELD_MISSING = "Missing mandatory field! Could not create document"
    DUPLICATE_DOCUMENT_REJECTED = (
        "Request results in creating a duplicate document, this is disallowed"
    )
    MODIFY_DOCUMENT_FAILED = "Could not update/delete the document"
    DOCUMENT_NOT_FOUND = "Document not found in DB"
    UNHANDLED_ERROR = "Unhandled exception occurred"
    MULTIPLE_DOCUMENT_FOUND = "Multiple document found"
    INVALID_TYPE_GIVEN = "Expected field type is not matching"
    OBJECT_CREATION_FAILED = "Object creation failed"

    ARGUMENT_RESOLUTION_FAILED = "Missing required arguments"
    DATA_TRANSFORM_FAILED = "Data Transform Failed"
    NOT_AT_EXPECTED_LOCATION = "Not At Expected Location"
    WEBSOCKET_ERROR = "Error in websocket"
    DOCUMENT_IN_USE = "Document is using some other collection as a foreign key"
    INVALID_FILE_TYPE = "Invalid file type selected"


class ValidationStudioError(HTTPException):
    """Generic exception class for the project. Formats exceptions the way FastApi needs them to be."""

    def __init__(
        self, error_code: ErrorCodes, location: Tuple, status_code: int = 422, detail=""
    ):
        """
        Constructor for the exception class
        :param error_code: Has to be an option from the enum
        :param location: should provide details on where the error occurred to be able to debug
        :param status_code: HTTP Status code
        """
        self.error_code = error_code
        self.location = location
        detail = [
            {
                "loc": location,
                "msg": (
                    f"{error_code.value}"
                    if not detail
                    else f"{error_code.value}. {detail}"
                ),
                "type": "validation_studio_error.semantic",
            }
        ]
        super().__init__(status_code=status_code, detail=detail)


class MongoError(Exception):
    """Generic error class for handling Mongo DB errors"""

    def __init__(self, error_code: ErrorCodes, description=None):
        self.error_code = error_code
        self.description = description
        super().__init__()

    def __str__(self):
        return f"<MongoError({self.error_code}, {self.description})>"
