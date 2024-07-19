"""
    Module: organisations.py
    Author: Rahul George

    Description:

    License:

    Created on: 10-06-2024

"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from ValidationStudioCloud.utils.bson_object_id import PydanticObjectId


class Organisation(BaseModel):
    """Device model"""

    id: PydanticObjectId = Field("", alias="_id")
    name: str
    is_archived: Optional[bool] = Field(False)
    is_deleted: Optional[bool] = Field(False)
    created_by: Optional[str] = None
    created_on: Optional[datetime] = None
    org_owner_email: EmailStr
    last_updated: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        """Config class"""

        arbitrary_types_allowed = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "666b578aba5977cc5816b8b7",
                "name": "Anora",
                "is_archived": False,
                "is_deleted": False,
                "org_owner_email": "",
                "created_by": "name",
                "updated_by": "name",
            }
        }
        key_fields: set = {"name", "org_owner_email"}
        id_fields: set = {"id"}

    class FilterBy(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        name: Optional[str] = None
        is_archived: Optional[bool] = None
        is_deleted: Optional[bool] = None
        created_by: Optional[str] = None
        created_on: Optional[datetime] = None
        org_owner_email: Optional[str] = None
        last_updated: Optional[datetime] = None
        updated_by: Optional[str] = None

        class Config:
            """Config class"""

            arbitrary_types_allowed = True
            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": "666b578aba5977cc5816b8b7",
                    "name": "Anora",
                    "is_archived": False,
                    "is_deleted": False,
                    "created_by": "name",
                    "org_owner_email": "",
                    # "last_updated": "time",
                    "updated_by": "name",
                }
            }

    class Unset(BaseModel):
        """A sub model, to be used for read operations.
        This is added because for query operation all the fields are optional while for
        other operations, this is not the case"""

        id: Optional[int] = Field(alias="_id", default=1)
        name: Optional[int] = 1
        is_archived: Optional[int] = 1
        is_deleted: Optional[int] = 1
        created_by: Optional[int] = 1
        created_on: Optional[int] = 1
        org_owner_email: Optional[int] = 1
        last_updated: Optional[int] = 1
        updated_by: Optional[int] = 1

        class Config:
            """Config class"""

            populate_by_name = True
            json_schema_extra = {
                "example": {
                    "id": 1,
                    "name": 1,
                    "is_archived": 1,
                    "is_deleted": 1,
                    "created_on": 1,
                    "created_by": 1,
                    "org_owner_email": 1,
                    "last_updated": 1,
                    "updated_by": 1,
                }
            }


# if __name__ == "__main__":
#     # device = Device.__get_pydantic_json_schema__()
#     import bson
#
#     o = Organisation(_id=bson.ObjectId(), name="Anora")
#     print(o.model_dump())
#
#     o_data = {'id': '666b578aba5977cc5816b8b7', 'name': 'Anora', 'is_archived': False}
#     o = Organisation(**o_data)
#     print(o)

"""
# TODO: Test whether Config class works


class OrgCRUD:
    def create_document(self):
        pass

    def create_embedded_document(self):
        pass

    def update_document(self):
        pass

    def update_embedded_document(self):
        pass

    def delete_document(self):
        pass

    def delete_embedded_document(self):
        pass

    def read_document(self):
        pass

    def read_embedded_document(self):
        pass


Document = TypeVar('Document')

class CRUDBase: ...


class DocumentCRUDBase:
    def create_document(self):
        pass

    def read_document(self):
        pass

    def update_document(self):
        pass

    def delete_document(self):
        pass


class EmbeddedDocumentCRUDBase(Generic[Document]):
    def create_embedded_document(self, document: Document):
        pass

    def read_embedded_document(self) -> List[Document]:
        pass

    def update_embedded_document(self):
        pass

    def delete_embedded_document(self):
        pass


class User(DocumentCRUDBase):
    pass

class Instruction(DocumentCRUDBase):
    pass

class InstructionArguments(EmbeddedDocumentCRUDBase):
    pass

user = User()
user.create_document()




class DeleteDocument:
    def delete(self):
        pass

class ReadDocument:
    def read(self):
        pass

class UpdateDocument: ...

class CreateDocument: ...

class DeleteEmbeddedDocument: ...

class ReadEmbeddedDocument: ...

class UpdateEmbeddedDocument: ...

class CreateEmbeddedDocument: ...


class User(DeleteDocument, ReadDocument, UpdateDocument, CreateDocument): ...

user = User()
user.read()
user.delete()
"""
