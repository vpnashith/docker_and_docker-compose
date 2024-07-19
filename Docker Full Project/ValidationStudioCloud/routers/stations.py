"""
    Module: stations.py
    Author: Radhika Krishnan

    Description: Routers for the stations class

    License:

    Created on: 05-07-2024

"""

import datetime
from typing import List

import bson
from fastapi import APIRouter, Body, Depends, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.stations import Stations
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import (
    convert_str_id_to_object_id,
    process_data,
    soft_delete_pre_check,
)
from ValidationStudioCloud.utils.exceptions import ValidationStudioError, ErrorCodes

router = APIRouter(prefix="/stations", tags=["Stations"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Stations.FilterBy],
    response_model_exclude_unset=True,
)
async def search_stations(
    filter_model: FilterModel[Stations.FilterBy, Stations.Unset],
    db_instance=Depends(get_database),
):
    """API for search stations"""
    content = await rcu.read_documents(
        db_instance["stations"],
        convert_str_id_to_object_id(
            Stations,
            filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
        ),
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Stations])
async def create_stations(stations: Stations, db_instance=Depends(get_database)):
    """
    API for create operation in Stations Collection
    """

    station = await process_data(
        Stations,
        db_instance,
        stations.model_dump(exclude={"id", "is_deleted"}),
    )

    if not station.get("created_by"):
        raise ValidationStudioError(
            ErrorCodes.MANDATORY_FIELD_MISSING,
            ("routers", "update"),
            detail="Create can't proceed without created by",
        )

    station["created_on"] = datetime.datetime.now()
    station["last_updated"] = datetime.datetime.now()
    station["is_deleted"] = False

    content = await rcu.create_document(
        db_instance["stations"], station, Stations.Config.key_fields
    )
    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Stations)
async def update_stations(
    station: Stations.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in stations collection
    """

    stations = await process_data(
        Stations,
        db_instance,
        station.model_dump(
            exclude={"id", "created_on", "created_by"}, exclude_unset=True
        ),
    )

    stations["last_updated"] = datetime.datetime.now()
    await soft_delete_pre_check(doc_id, stations, db_instance, "stations")

    content = await rcu.update_document(
        db_instance["stations"],
        bson.ObjectId(doc_id),
        stations,
        Stations.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stations(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation for stations
    """

    content = await rcu.delete_document(db_instance["stations"], bson.ObjectId(doc_id))
    return content
