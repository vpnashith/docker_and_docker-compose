
# pylint: disable=R0913

from typing import Dict, Any, List, Set, Union, Optional

from bson import ObjectId
from pymongo.collection import Collection

import ValidationStudioCloud.utils.mongo_utils as mu
from ValidationStudioCloud.utils.exceptions import (
    ErrorCodes,
    MongoError,
    ValidationStudioError,
)


async def read_documents(
    collection_instance: Collection, filter_by: Dict[str, Any], projection=None
) -> List[Dict[Any, Any]]:
    """
    generic method to read documents from db
    """
    if projection is None:
        projection = {}
    return_data = mu.read_document(collection_instance, filter_by, projection)
    if len(return_data) > 0 and return_data[0].get("is_deleted") is None:
        return return_data
    filtered_data = list(
        filter(
            (lambda dic: not dic.get("is_deleted")),
            return_data,
        )
    )

    return filtered_data


async def create_document(
    collection_instance: Collection,
    document: Dict[Any, Any],
    key_fields: Set,
    allow_duplicates: bool = False,
) -> List[Dict[Any, Any]]:
    """
    Create a new document in the DB.

    Todo: When document contains other id fields, we need to verify the foregin keys exists or not.

    :param allow_duplicates:
    :param key_fields:
    :param document:
    :param collection_instance:
    :return: Return the created device.
    """
    try:
        response = mu.create_document(
            collection_instance, document, key_fields, allow_duplicates
        )
    except MongoError as err:
        location = ("rest_controller_utils", "create")
        raise ValidationStudioError(err.error_code, location) from err

    return response


async def update_document(
    collection_instance: Collection,
    doc_id: Union[str, ObjectId],
    document: Dict[Any, Any],
    key_fields: Set,
    allow_duplicates: bool = False,
) -> Dict[Any, Any]:
    """
    generic method to update documents in db
    """
    try:
        response = mu.update_document(
            collection_instance, doc_id, document, key_fields, allow_duplicates
        )
    except MongoError as err:
        location = ("rest_controller_utils", "update")
        raise ValidationStudioError(err.error_code, location) from err

    return response


async def delete_document(
    collection_instance: Collection, doc_id: Union[str, ObjectId], id_field: str = "_id"
) -> bool:
    """
    generic method to delete documents from db
    """
    try:
        content = mu.delete_document(collection_instance, doc_id, id_field)
    except MongoError as err:
        location = ("rest_controller_utils", "delete")
        raise ValidationStudioError(err.error_code, location) from err

    if content:
        return True

    raise ValidationStudioError(
        ErrorCodes.MODIFY_DOCUMENT_FAILED, location=("rest_controller_utils", "delete")
    )


async def read_embedded_document(
    collection_instance: Collection,
    doc_id: Union[str, ObjectId],
    embedded_field: str,
    embedded_field_filter: Dict[str, Any],
    embedded_field_projection: {},
) -> List[Dict[Any, Any]]:
    """
    generic method to read documents in db
    """
    doc_id = {"_id": mu.get_object_id(doc_id)}

    embedded_field_projection_dict = {}
    for key, val in embedded_field_projection.items():
        if not key.startswith(f"{embedded_field}."):
            embedded_field_projection_dict[f"{embedded_field}.{key}"] = val
        else:
            embedded_field_projection_dict[key] = val
    # embedded_field_projection_dict["_id"] = 0

    embedded_filter = {}
    for field in embedded_field_filter:
        embedded_filter[f"{embedded_field}.{field}"] = embedded_field_filter[field]
    try:
        db_result = mu.read_embedded_document(
            collection_instance,
            doc_id,
            embedded_field,
            embedded_filter,
            embedded_field_projection_dict,
        )
    except MongoError as err:
        location = ("rest_controller_utils", "read_embedded")
        raise ValidationStudioError(err.error_code, location) from err
    content = []
    for sub_doc in db_result:
        if "_id" in sub_doc:
            sub_doc.pop("_id")
            content.append(sub_doc[embedded_field])

    return content


async def update_embedded_document(
    collection_instance: Collection,
    document_filter: Dict[str, Any],
    embedded_doc_filter: Dict[str, Any],
    embedded_field: str,
    doc: Dict,
    key_fields: set,
) -> List[Dict[Any, Any]]:  # pylint: disable=R0913
    """
    generic method to update documents in db
    """

    for key, val in embedded_doc_filter.items():
        if not key.startswith(f"{embedded_field}."):
            document_filter[f"{embedded_field}.{key}"] = val
        else:
            document_filter[key] = val

    doc_dict = {}
    for key, val in doc.items():
        if not key.startswith(f"{embedded_field}.$."):
            doc_dict[f"{embedded_field}.$.{key}"] = val
        else:
            doc_dict[key] = val
    try:
        result = mu.update_embedded_document(
            collection_instance, document_filter, doc_dict, embedded_field, key_fields
        )
    except MongoError as err:
        location = ("rest_controller_utils", "update_embedded")
        raise ValidationStudioError(err.error_code, location) from err
    content = []
    for sub_doc in result[0][embedded_field]:
        if sub_doc["_id"] == embedded_doc_filter["_id"]:
            content.append(sub_doc)
    return content


async def create_embedded_document(
    collection_instance: Collection,
    doc_id: Union[str, ObjectId],
    embedded_field: str,
    document: Dict[str, Any],
    key_fields: set,
    position: Optional[int] = None,
) -> List[Dict[Any, Any]]:  # pylint: disable=R0913
    """
    generic method to create embedded documents in db
    """
    doc_id = {"_id": mu.get_object_id(doc_id)}
    try:
        response = mu.insert_embedded_document(
            collection=collection_instance,
            document_filter=doc_id,
            embedded_field=embedded_field,
            embedded_doc=document,
            position=position,
            allow_duplicates=False,
            key_fields=key_fields,
        )

    except MongoError as err:
        location = ("rest_controller_utils", "embedded create")
        raise ValidationStudioError(err.error_code, location) from err

    content = []
    for sub_doc in response[0][embedded_field]:
        if sub_doc["_id"] == document["_id"]:
            content.append(sub_doc)
    return content


async def delete_embedded_document(
    collection_instance: Collection,
    document: Dict[str, ObjectId],
    delete_condition: Dict[str, Union[str, Any]],
) -> bool:
    """
    generic method to delete embedded documents in db
    """
    try:
        response = mu.delete_embedded_document(
            collection=collection_instance,
            document_filter=document,
            delete_condition=delete_condition,
        )

    except MongoError as err:
        location = ("rest_controller_utils", "embedded delete")
        raise ValidationStudioError(err.error_code, location) from err

    if response:
        return True

    raise ValidationStudioError(
        ErrorCodes.MODIFY_DOCUMENT_FAILED,
        location=("rest_controller_utils", "embedded delete"),
    )
