"""
    Module: organisations

    Created on: 08-07-2024

"""
# flake8: noqa
# pylint: disable=C0302
# pylint:disable=C0301,W0012,W1401,W0012,C0206,R1735, R0914, R1703, R0912,  R0915, W0612,W0719, W1404
# pylint: disable=duplicate-code
# pylint: disable=R0915
# pylint: disable=C0103
# pylint: disable=W0612

from ValidationStudioCloud.db_creator.helper_functions import insert_docs

# pylint:disable =  W0613


def create_organisations(my_db):
    """Contain all the organisations data"""
    organisations = [
        {
            "name": "OrgName",
            "is_archived": False,
            "is_deleted": False,
            "created_by": "User1",
            "updated_by": "User2",  
        }
    ]

    return insert_docs(my_db, "organisations", organisations)
