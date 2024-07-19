"""
    Module: test_organisations
    Author: Sweeda Noronha

    Description: Pytest for testing organisations endpoints

    License:

    Created on: 08-07-2024

"""

import bson
from bson import ObjectId

from fastapi.encoders import jsonable_encoder
from ValidationStudioCloud.db_creator.db_creator_main import main
from ValidationStudioCloud.tests.pytest_helpers import (  # noqa: F401
    fixture_client as client,
)
from ValidationStudioCloud.tests.pytest_helpers import generate_db_instance


# pylint: disable=duplicate-code

# ------------------------------------------------------------
#                   Get Organisations
# ------------------------------------------------------------


def test_get_organisations_no_filter(client):  # noqa: F811
    """Test whether end point is able to read organisations details from database"""
    main()
    db_instance = generate_db_instance()
    data = {
        "filter_by": {},
        "unset": {},
    }
    response = client.post("/organisations/search", json=data)

    data_cursor = db_instance["organisations"].find({})

    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor), custom_encoder={bson.ObjectId: str}
    )
    assert response.json() == data_cursor_serialised
    db_instance.client.close()


def test_get_organisations_with_filter(client):  # noqa: F811
    """Test whether end point is able to read organisations details from database"""
    main()
    db_instance = generate_db_instance()
    data = {"filter_by": {"name": "OrgName"}, "unset": {}}
    response = client.post("/organisations/search", json=data)
    data_cursor = db_instance["organisations"].find({"name": "OrgName"})

    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor), custom_encoder={bson.ObjectId: str}
    )
    assert response.json() == data_cursor_serialised

    data_2 = {"filter": {"name": "OrgName", "created_by": "User1", "is_deleted": False}}
    response = client.post("/organisations/organisations/search", json=data_2)
    data_cursor_1 = db_instance["organisations"].find(
        {"name": "OrgName", "created_by": "User1", "is_deleted": False}
    )

    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor_1), custom_encoder={bson.ObjectId: str}
    )
    assert response.json() == data_cursor_serialised

    data_3 = {"filter": {"created_by": "User1"}}
    response = client.post("/organisations/organisations/search", json=data_3)
    data_cursor_2 = db_instance["organisations"].find({"created_by": "User1"})

    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor_2), custom_encoder={bson.ObjectId: str}
    )
    assert response.json() == data_cursor_serialised

    # Trying to filter a value not in DB, should not throw error

    data = {"filter": {"created_by": "User2"}, "unset": {}}
    response = client.post("/organisations/organisations/search", json=data)
    data_cursor1 = db_instance["organisations"].find({"created_by": "User2"})

    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor1), custom_encoder={bson.ObjectId: str}
    )
    assert response.json() == data_cursor_serialised

    # Create more of this test combinations


def test_get_organisations_with_unset_and_filter(client):  # noqa: F811
    """Test whether end point is able to read organisations details from database"""
    main()
    db_instance = generate_db_instance()
    data = {"filter": {"name": "OrgName"}, "unset": {"created_by": 0, "_id": 0}}
    response = client.post("/organisations/organisations/search", json=data)
    data_cursor = db_instance["organisations"].find(
        {"name": "OrgName"}, {"created_by": "User1", "_id": 0}
    )
    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor), custom_encoder={bson.ObjectId: str}
    )
    response_json = response.json()
    assert response_json == data_cursor_serialised
    assert "created_by" not in response_json[0]
    assert "_id" not in response_json[0]

    data = {
        "filter": {"name": "OrgName", "created_by": "User1"},
        "unset": {"name": 0, "created_by": 0},
    }
    response = client.post("/organisations/organisations/search", json=data)
    data_cursor = db_instance["organisations"].find(
        {"name": "OrgName", "created_by": "User1"}, {"name": 0, "created_by": 0}
    )
    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor), custom_encoder={bson.ObjectId: str}
    )
    response_json = response.json()
    assert response_json == data_cursor_serialised
    assert "name" not in response_json[0]
    assert "created_by" not in response_json[0]

    # Unset field not in database, should not throw error.

    data = {"filter": {"name": "OrgName"}, "unset": {"db_key": 0}}
    response = client.post("/organisations/organisations/search", json=data)

    data_cursor1 = db_instance["organisations"].find({"name": "OrgName"}, {"db_key": 0})

    assert response.status_code == 200
    data_cursor_serialised = jsonable_encoder(
        list(data_cursor1), custom_encoder={bson.ObjectId: str}
    )
    response_json = response.json()
    assert response_json == data_cursor_serialised
    db_instance.client.close()


def test_get_organisations_filter_with_id(client):  # noqa: F811
    """Test whether end point is able to read organisations details from database"""
    main()
    db_instance = generate_db_instance()
    data = {"filter": {"name": "OrgName", "created_by": "User1"}, "unset": {}}
    response = client.post("/organisations/organisations/search", json=data)
    expected_json = response.json()
    org_id = expected_json[0]["_id"]

    data = {"filter": {"_id": str(org_id)}, "unset": {}}
    response = client.post("/organisations/organisations/search", json=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == expected_json
    db_instance.client.close()


def test_get_organisations_with_incorrect_field(client):  # noqa: F811
    """Test whether end point is able to read organisations details from database"""
    main()
    data = {"filter": {"orgname": "OrgName"}, "unset": {}}
    response = client.post("/organisations/organisations/search", json=data)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json == {
        "detail": [
            {
                "loc": ["parse_filter", "Get", "validation"],
                "msg": "unknown field supplied for model. Parsing Failed. ('orgname',) "
                ": extra fields not permitted",
                "type": "ValidationStudioCloud_error.semantic",
            }
        ]
    }


# ------------------------------------------------------------
#                   Create organisations
# ------------------------------------------------------------


def test_create_organisations(client):  # noqa: F811
    """Test whether end point is able to create new organisations"""
    main()
    data = {
        "name": "OrgName1",
        "is_archived": False,
        "is_deleted": False,
        "created_by": "User1",
        "updated_by": "User2",
    }
    response = client.post("/organisations/organisations", json=data)

    assert response.status_code == 201
    response_json = response.json()
    assert response_json[0]["name"] == "OrgName1"


def test_create_organisations_missing_required(client):  # noqa: F811
    """Test whether end point is able to create new organisations"""
    main()

    data = {"created_by": "User2"}
    response = client.post("/organisations/organisations", json=data)

    assert response.status_code == 422
    result = response.json()
    assert result["detail"][0]["msg"] == "field required"


def test_create_organisations_missing_optional(client):  # noqa: F811
    """Test whether end point is able to create new organisations"""
    main()
    data = {"name": "OrgName1"}
    response = client.post("/organisations/organisations", json=data)

    assert response.status_code == 201
    response_json = response.json()
    assert response_json[0]["name"] == "OrgName1"
    assert response_json[0]["is_deleted"] is False


def test_create_organisations_duplicate(client):  # noqa: F811
    """Test whether end point is able to create new organisations"""
    main()
    data_for_organisations = {
        "filter": {"name": "OrgName1", "created_by": "User1"},
        "unset": {"release_stage": 0},
    }
    response = client.post(
        "/organisations/organisations/search", json=data_for_organisations
    )
    assert response.status_code == 200
    data = {
        "name": "OrgName1",
        "created_by": "User1",
        "updated_by": "User2",
        "is_deleted": False,
    }
    response = client.post("/organisations/organisations", json=data)

    assert response.status_code == 422
    result = response.json()
    assert (
        result["detail"][0]["msg"]
        == "Request results in creating a duplicate document, this is disallowed"
    )


# ------------------------------------------------------------
#                   Update organisations
# ------------------------------------------------------------


def test_update_organisations(client):  # noqa: F811
    """Test whether endpoint can update organisations details"""
    main()

    # Read the data first.
    data = {
        "filter": {"name": "OrgName", "created_by": "User1", "updated_by": "User2"},
        "unset": {},
    }
    response = client.post("/organisations/organisations/search", json=data)
    result = response.json()
    org_id = result[0]["_id"]

    data = {
        "organisations": {
            "name": "OrgName",
            "created_by": "User1",
            "updated_by": "User3",
        },
        "doc_id": str(org_id),
    }

    response = client.put("/organisations/organisations", json=data)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["updated_by"] == "User3"


def test_update_organisations_duplicate(client):  # noqa: F811
    """Test whether endpoint can update organisations details"""
    main()
    # Read the data first.
    data = {"filter": {"name": "Orgname"}, "unset": {}}
    response = client.post("/organisations/organisations/search", json=data)
    result = response.json()

    data = {
        "organisations": {
            "name": "OrgName",
            "is_archived": False,
            "is_deleted": False,
            "created_by": "User1",
            "updated_by": "User2",
        },
        "doc_id": str(result[0]["_id"]),
    }

    response = client.put("/organisations/organisations", json=data)

    assert response.status_code == 422
    result = response.json()
    assert (
        result["detail"][0]["msg"]
        == "Request results in creating a duplicate document, this is disallowed"
    )


def test_update_organisations_incorrect_organisations_id(client):  # noqa: F811
    """Test whether endpoint can update organisations details"""
    main()

    object_id = ObjectId()

    data = {
        "organisations": {"name": "OrgName", "craeted_by": "User1"},
        "doc_id": str(object_id),
    }

    response = client.put("/organisations/organisations", json=data)

    assert response.status_code == 422
    result = response.json()
    assert result["detail"][0]["msg"] == "Document not found in DB"


# ------------------------------------------------------------
#                   Delete organisations
# ------------------------------------------------------------


def test_delete_organisations_incorrect_id(client):  # noqa: F811
    """Test whether endpoint can delete organisations details"""
    main()
    object_id = ObjectId()

    data = {"doc_id": str(object_id)}

    response = client.delete("/organisations/organisations", json=data)

    assert response.status_code == 422
    result = response.json()
    assert result["detail"][0]["msg"] == "Document not found in DB"


def test_delete_organisations_correct_id(client):  # noqa: F811
    """Test whether endpoint can delete organisations details"""
    main()
    # Read the data first.
    data = {"filter": {"name": "OrgName"}, "unset": {"_id": 1}}
    response = client.post("/organisations/organisations/search", json=data)

    result = response.json()

    data = {"doc_id": str(result[0]["_id"])}

    response = client.delete("/organisations/organisations", json=data)

    assert response.status_code == 200
    result = response.json()
    assert result is True
