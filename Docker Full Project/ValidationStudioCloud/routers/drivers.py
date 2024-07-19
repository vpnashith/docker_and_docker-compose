"""
    Module: organisation_dept.py
    Author: Rahul George

    Description:

    License:

    Created on: 13-06-2024

"""

import os
from typing import List, Optional
import bson
from fastapi import APIRouter, Body, Depends, status, UploadFile, File

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.drivers import Drivers
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id
from ValidationStudioCloud.utils.exceptions import ValidationStudioError, ErrorCodes
from ValidationStudioCloud.settings import settings

router = APIRouter(prefix="/instruments/drivers", tags=["Drivers"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Drivers.FilterBy],
    response_model_exclude_unset=True,
)
async def search_drivers(
    filter_model: FilterModel[Drivers.FilterBy, Drivers.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for search drivers in instruments collection
    """
    filter_by_dict = convert_str_id_to_object_id(
        Drivers,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )
    content = await rcu.read_embedded_document(
        db_instance["instruments"],
        doc_id,
        "drivers",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Drivers])
async def create_drivers(
    driver: Drivers,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API to create driver in instruments collection
    """
    driver_data = convert_str_id_to_object_id(
        Drivers, driver.model_dump(exclude_unset=True, by_alias=True, exclude={"id"})
    )
    driver_data["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["instruments"],
        doc_id,
        "drivers",
        driver_data,
        driver.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Drivers])
async def update_driver(
    driver: Drivers.FilterBy,
    doc_id: str = Body(..., embed=True),
    driver_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API to update driver in instruments collection
    """
    key_fields = Drivers.Config.key_fields

    content = await rcu.update_embedded_document(
        db_instance["instruments"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(driver_id)},
        "drivers",
        convert_str_id_to_object_id(
            Drivers, driver.model_dump(exclude_unset=True, exclude={"id"})
        ),
        key_fields,
    )

    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    doc_id: str = Body(..., embed=True),
    driver_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API to delete operation in device collection
    """
    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["instruments"],
        document=document_filter,
        delete_condition={"drivers": {"_id": bson.ObjectId(driver_id)}},
    )

    return content


@router.post("/file_upload", status_code=status.HTTP_200_OK)
async def upload_driver(
    instrument_id: str,
    driver_id: str,
    file: UploadFile = File(...),
    db_instance=Depends(get_database),
):
    """
    Upload driver file
    """

    driver_path = str(settings.DRIVER_PATH)
    os.makedirs(driver_path, exist_ok=True)

    file_location = os.path.join(driver_path, file.filename)
    if not file.filename.endswith(".py"):
        raise ValidationStudioError(
            ErrorCodes.INVALID_FILE_TYPE, ("drivers", "file_upload")
        )

    content = await rcu.read_embedded_document(
        db_instance["instruments"],
        bson.ObjectId(instrument_id),
        "drivers",
        {"_id": bson.ObjectId(driver_id)},
        {},
    )

    if not content:
        raise ValidationStudioError(
            ErrorCodes.DOCUMENT_NOT_FOUND, ("drivers", "file_upload")
        )

    with open(file_location, "wb") as _file:
        _file.write(await file.read())

    [existing_data] = content
    existing_data.pop("_id")
    existing_data["driver_path"] = file_location
    updated_data = await rcu.update_embedded_document(
        db_instance["instruments"],
        {"_id": bson.ObjectId(instrument_id)},
        {"_id": bson.ObjectId(driver_id)},
        "drivers",
        existing_data,
        Drivers.Config.key_fields,
    )
    updated_data[0]["_id"] = str(updated_data[0]["_id"])
    return updated_data
