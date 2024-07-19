"""
    Module: mongo_helper.py
    Author: Rahul George

    Description:

    License:

    Created on: 28-07-2022

"""
import uuid
from typing import Union, Dict, List, Optional, Any, Set

from bson import ObjectId
from pymongo.collection import Collection, ReturnDocument

from ValidationStudioCloud.utils.exceptions import MongoError, ErrorCodes


def get_object_id(doc_id: Union[str, ObjectId]):
    """Helper method to convert string to ObjectId type"""
    if isinstance(doc_id, str):
        doc_id = ObjectId(doc_id)
    elif not isinstance(doc_id, (uuid.UUID, ObjectId)):
        raise MongoError(ErrorCodes.INVALID_TYPE_GIVEN)

    return doc_id


def validate_missing_fields(document, key_fields: set):
    """
    Helper function to evaluate if the document contains all the key_fields.
    The method does not check if the value of the key_field is None or not.

    Args:
        document:
        key_fields:

    Returns:


    """

    # Does not handle nested documents. But pydantic also does the validation, how is this different?
    for field in key_fields:
        if field not in document:
            raise MongoError(ErrorCodes.MANDATORY_FIELD_MISSING)  # to be modified to handle errors better


def read_document(collection: Collection, query_filter=None, projection=None) -> List[Dict]:
    """
    Filter a collection based on the higher level field filters

    Args:
        collection: instance pointing to the right database table
        query_filter: dictionary of field and value to filter
        projection: field names to include or exclude in result

    Returns:
        List

    Examples:

        my_db['user_device_configurations'].find({'name': 'Bandgap study'}, {})

    """
    if projection is None:
        projection = {}
    if query_filter is None:
        query_filter = {}

    cursor = collection.find(filter=query_filter, projection=projection)
    return list(cursor)


def create_document(collection: Collection, document: Dict, key_fields: Optional[set], allow_duplicates: bool = False):
    """
    Function create a document in the DB and return the complete document back.
    Args:
        allow_duplicates:
        key_fields:
        collection:
        document:

    Returns:

    Examples:

        my_db['user_device_configurations'].insert_one({'name': 'Bandgap study', 'type': "123"})
    """
    if key_fields is None:
        key_fields = {}

    validate_missing_fields(document, key_fields)

    if not allow_duplicates:
        # Check whether another document exists with same key_fields
        query_filter = dict((field, document[field]) for field in key_fields)
        result = read_document(collection, query_filter)
        if result:
            raise MongoError(ErrorCodes.DUPLICATE_DOCUMENT_REJECTED)

    response = collection.insert_one(document)
    result = read_document(collection, {"_id": response.inserted_id})

    return result


def update_document(
        collection: Collection,
        doc_id: Union[str, ObjectId],
        document: Dict,
        key_fields: Optional[Set],
        allow_duplicates: bool = False,
        id_field="_id",
):  # pylint: disable=R0913
    """
    Fetches a document from the DB Collection and updates this.
    Also, validates if the modification creates a duplicate entry or not,
    and can abort the modification if ``allow_duplicates`` = False


    # Read the document from the DB based on the id
    # Compare the key fields vs with one on DB
    # If there are no changes to key fields, skip the duplicate check, because we are modifying optional fields.
    # How are we tackling the scenario when embedded document is present?
        # It does not matter, key fields are only for the outer document at this level.
    * Is it necessary to check missing fields?
        # No, because we may want to update only one field sometimes.

    Args:
        id_field: Specify the field to use as id field. Default is '_id'
        collection: Name of the collection
        doc_id: Value of the doc id field, with which filtering has to be done.
        document:
        key_fields:
        allow_duplicates:

    Returns:

    """

    if key_fields is None:
        key_fields = {}

    # Read the original document, if not present raise error
    documents_in_db = read_document(collection, query_filter={id_field: get_object_id(doc_id)}, projection=key_fields)
    if not documents_in_db:
        raise MongoError(ErrorCodes.DOCUMENT_NOT_FOUND)
    document_in_db = documents_in_db[0]

    # Decide if duplicate check is required.
    perform_duplicate_check = False
    if not allow_duplicates:
        for field in key_fields:
            if field not in document:  # Field is not sent by the caller, user does not intend to modify this field
                document[field] = document_in_db[field]
            elif document_in_db[field] != document[field]:  # if key field values are different, perform duplicate check
                perform_duplicate_check = True

    if perform_duplicate_check:
        # Check whether another document exists with same key_fields
        query_filter = dict((field, document[field]) for field in key_fields)
        result = read_document(collection, query_filter)
        if result:
            raise MongoError(ErrorCodes.DUPLICATE_DOCUMENT_REJECTED)

    return collection.find_one_and_update(
        {id_field: get_object_id(doc_id)},
        {"$set": document},
        return_document=ReturnDocument.AFTER,
    )


def delete_document(collection: Collection, doc_id: Union[str, ObjectId, uuid.UUID], id_field="_id"):
    """
    Check if the document with the given id is present in the DB.
    If found, delete it.
    else raise exception

    Args:
        id_field:
        collection:
        doc_id:

    Returns:

    """
    # Read the original document, if not present raise error
    documents_in_db = read_document(collection, query_filter={id_field: get_object_id(doc_id)})

    if not documents_in_db:
        raise MongoError(ErrorCodes.DOCUMENT_NOT_FOUND)

    response = collection.find_one_and_delete({id_field: get_object_id(doc_id)})

    if not response:
        raise MongoError(ErrorCodes.DOCUMENT_NOT_FOUND)

    return True


def delete_embedded_document(
        collection, document_filter: Dict[str, Union[str, ObjectId]], delete_condition: Dict[str, Union[str, Any]]
):
    """
    Check if embedded document exists. if more than one document is obtained raise exception.

    Args:
        document_filter: Dictionary to filter the correct sub doc.
        delete_condition: Condition to be given to perform the update
        collection: Instance of the MongoDB Collection

    Returns:

    Examples:

        Two level embedded document
        document_filter = {'_id': ObjectId('62e2e811c66d42dfba07dd6e'),
               'configuration_steps.step_id': ObjectId('62e2e811c66d42dfba07dd6a')}
        update_condition = {
            '$pull': {
                'configuration_steps.$.tokens':
                    {'order': '1'}
            }
        }
        response = collection.update_one(document_filter,
                                         update_condition)

        One level embedded document

        document_filter = {'_id': ObjectId('62e2e811c66d42dfba07dd6e')}
        update_condition = {
            '$pull': {
                'configuration_steps':
                    {'step_id': ObjectId('62e2e811c66d42dfba07dd6f')}
            }
        }

        response = collection.update_one(document_filter,
                                         update_condition)
    """
    update_condition = {"$pull": delete_condition}

    response = collection.update_one(document_filter, update_condition)
    if response.modified_count == 0:
        raise MongoError(ErrorCodes.DOCUMENT_NOT_FOUND)
    if response.matched_count > 1:
        print("Matched more than one document with the given condition!! ")
    return True


def update_embedded_document(
        collection,
        document_filter: Dict[str, Any],
        doc: Dict,
        embedded_field=None,
        key_fields=None,
        allow_duplicates: bool = False,
):  # pylint: disable=W0613,  R0913
    """

    Args:
        collection:
        document_filter:
        doc:
        embedded_field:
        key_fields:
        allow_duplicates:

    Returns:

    Examples:
        Update fields of an embedded document: Update Specific document with id
        response = my_db['user_device_conf'].update_many({'_id': ObjectId('62e2e811c66d42dfba07dd6e'
                                            'configuration_steps.step_id': ObjectId('62e2e811c66d42dfba07dd6f')},
                                     {'$set': {'configuration_steps.$.action_type': 'macro1',
                                           'configuration_steps.$.action_id': '123'}})

        Update fields of an embedded document: Update all sub docs
        response = my_db['user_device_conf'].update_many({'_id': ObjectId('62e2e811c66d42dfba07dd6e')},
                                          {'$set': {'configuration_steps.$[].action_type': 'macro1'}})

        Update fields of an embedded document: Update all sub docs with another doc/list
        We need document_filter, field, value
        response = my_db['user_device_conf'].update_many({'_id': ObjectId('62e2e811c66d42dfba07dd6e')},
                                        {'$set': {'configuration_steps.$[].action_type': [{'name': 'rtg'}]}})

        Update fields of an embedded document: Update all sub docs with another doc/list multiple fields
        We need document_filter, field, value
        response = my_db['user_device_conf'].update_many({'_id': ObjectId('62e2e811c66d42dfba07dd6e')},
                                       {'$set': {'configuration_steps.$[].action_type': [{'name': 'rtg'}],
                                                    'configuration_steps.$[].head': None}})
    """
    # `allow_duplicates` functionality is not implemented.
    read_response = None
    if key_fields:
        key_fields = {f"{embedded_field}.{key}" for key in key_fields}
    if not allow_duplicates:
        field_filter_doc = {key.replace(".$", ""): val for key, val in doc.items()}
        embedded_field_filter = {key: val for key, val in field_filter_doc.items() if key in key_fields}

        read_response = read_embedded_document(
            collection, {"_id": document_filter["_id"]}, embedded_field, embedded_field_filter, {}
        )
        if (
            len(read_response) > 0 and embedded_field_filter
            and document_filter[f"{embedded_field}._id"] != read_response[0][embedded_field]["_id"]
        ):
            raise MongoError(ErrorCodes.DUPLICATE_DOCUMENT_REJECTED)

    response = collection.update_many(document_filter, {"$set": doc})
    if response.modified_count == 0:
        for each_dict in read_response:
            if document_filter[f"{embedded_field}._id"] == each_dict[embedded_field]["_id"]:
                read_response = [each_dict]
                break
        check_response = check_doc_similarity(read_response, doc, embedded_field)
        if not check_response:
            read_response[0][embedded_field] = [read_response[0][embedded_field]]
            return read_response
        raise MongoError(ErrorCodes.MODIFY_DOCUMENT_FAILED)

    response = read_document(collection, query_filter=document_filter)
    if isinstance(response, list):
        return response
    return list(response)


def insert_embedded_document(
        collection,
        document_filter: Dict[str, Any],
        embedded_field: str,
        embedded_doc: Union[Dict, List],
        position: Optional[int] = None,
        allow_duplicates=False,
        key_fields: Optional[set] = None,
):  # pylint: disable=R0913
    """

    Args:
        key_fields:
        allow_duplicates:
        collection:
        document_filter:
        embedded_field:
        embedded_doc:
        position:

    Returns:

    Examples:
        Two level embedded document:
            document_filter = {'_id': ObjectId('62e2e811c66d42dfba07dd6e'),
            'configuration_steps.step_id': ObjectId('62e2e811c66d42dfba07dd6f')}

            field = 'configuration_steps.$.tokens'

            doc = [{'order': '2', 'value': 'abc'}]

        Single level embedded document:
            document_filter = {'_id': ObjectId('62e2e811c66d42dfba07dd6e')}
            field = 'configuration_steps'

            doc = [{'order': '2', 'value': 'abc'}]

        my_db['user_device_config'].update_many(document_filter,
                                                {'$push': { field: {'$each': doc }}})

    """
    document_list = embedded_doc if isinstance(embedded_doc, list) else [embedded_doc]
    if not key_fields:
        key_fields = {}
    if not allow_duplicates:
        # Check if an existing embedded document is present with same parameters
        embedded_field_filter = {key: value for key, value in embedded_doc.items() if key in key_fields}
        response = read_embedded_document(collection, document_filter, embedded_field, embedded_field_filter, {})
        if len(response) > 0:
            raise MongoError(ErrorCodes.DUPLICATE_DOCUMENT_REJECTED)

    if position is None:
        embedded_query = {embedded_field: {"$each": document_list}}
    else:
        embedded_query = {embedded_field: {"$each": document_list, "$position": position}}

    response = collection.update_many(document_filter, {"$push": embedded_query})
    if response.modified_count == 0:
        raise MongoError(ErrorCodes.MODIFY_DOCUMENT_FAILED)

    modified_document = read_document(collection, document_filter)

    return list(modified_document)


def read_embedded_document(
        collection,
        document_filter: Dict[str, Any],
        embedded_field: str,
        embedded_field_filter: Dict[str, Any],
        embedded_field_projection: Dict[str, int],
):
    """

    Args:
        embedded_field_projection:
        embedded_field_filter:
        embedded_field:
        collection:
        document_filter:

    Returns:

    Examples:
        document_filter = {'_id': ObjectId('62e39d68ee6528b6d2f78c1f') }
        projection = {'configuration_steps': 1}

        document_filter = {'_id': ObjectId('62e39d68ee6528b6d2f78c1f'), 'configuration_steps.action_type': 'macro'}
        projection = {'configuration_steps.$': 1}

    """

    embedded_filter = {}
    for key, value in embedded_field_filter.items():
        if not key.startswith(f"{embedded_field}."):
            embedded_filter[f"{embedded_field}.{key}"] = value
        else:
            embedded_filter[key] = value

    embedded_projection = {}
    for key, value in embedded_field_projection.items():
        if not key.startswith(f"{embedded_field}."):
            embedded_projection[f"{embedded_field}.{key}"] = value
        else:
            embedded_projection[key] = value

    pipeline = [{"$match": document_filter}, {"$project": {embedded_field: 1}}, {"$unwind": f"${embedded_field}"}]

    if embedded_filter:
        pipeline.append({"$match": embedded_filter})
    if embedded_projection:
        pipeline.append({"$project": embedded_projection})

    response = collection.aggregate(pipeline)
    ret = list(response)
    return ret


def check_doc_similarity(read_doc, check_doc, embedded_field):
    """
    method to check whether the updating sub doc is same as existing sub doc or not
    using while updating sub doc
    """
    update_check_doc = {}
    check_set = set()

    # separate the embedded filed name from the sub doc "<embd_field>.$." will be removed
    if embedded_field:
        for fields in check_doc:
            update_check_doc[fields[len(embedded_field) + 3 : :]] = check_doc[fields]  # noqa: E203

    # checks whether there is any new fields added other than existing
    for field in update_check_doc:
        if field not in read_doc[0][embedded_field].keys():
            check_set.add(field)

    # checking whether the updated value is same as existing value or not.
    # if not then the field adding to check_set
    for fields, value in update_check_doc.items():
        if value != read_doc[0][embedded_field][fields]:
            check_set.add(fields)
    return check_set


if __name__ == "__main__":
    pass
