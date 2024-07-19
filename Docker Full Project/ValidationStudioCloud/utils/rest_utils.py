"""
    Module: rest_utils.py
    Author: Rahul George

    Description: Supporting Pydantic Models for search api

    License:

    Created on: 01-11-2023

"""

# pylint: disable=C0103
# pylint: disable=E0611
# pylint: disable=R0903

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

DataTypeX = TypeVar("DataTypeX")
DataTypeY = TypeVar("DataTypeY")


class FilterModel(BaseModel, Generic[DataTypeX, DataTypeY]):
    """Model to accept the filters and ignore fields for querying the database"""

    filter_by: Optional[DataTypeX]
    unset: Optional[DataTypeY]

    class Config:
        """class config"""

        arbitrary_types_allowed = True


if __name__ == "__main__":
    # Code to test this module standalone

    class Product(BaseModel):
        """Product test model"""

        name: str
        description: Optional[str] = ""
        price: int

    class ProductUnset(BaseModel):
        """Product unset test model"""

        name: int = 1
        description: int = 1
        price: int = 1

    product = Product(name="P1", price=10)
    product_unset = ProductUnset(name=1)

    search = FilterModel[Product, ProductUnset](filter_by=product, unset=product_unset)
    print(search)

    search = FilterModel[Product, ProductUnset](filter_by=product, unset={})
    print(search)
    print(search.model_json_schema())

    search = FilterModel[Product, ProductUnset](unset=product_unset)
    print(search)
