"""
    Module: stations_instruments.py
    Author: Radhika Krishnan

    Description: Routers for the stations instruments class

    License:

    Created on: 10-07-2024
"""

from typing import Optional, List

import bson
from fastapi import APIRouter, Body, Depends, status
import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.stations_instruments import Instruments
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import process_data


router = APIRouter(
    prefix="/stations/station_instruments", tags=["Stations_instruments"]
)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Instruments.FilterBy],
    response_model_exclude_unset=True,
)
async def search_station_instruments(
    filter_model: FilterModel[Instruments.FilterBy, Instruments.Unset],
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """API for search operation in instruments: embedded field in stations collection"""

    filter_by_dict = await process_data(
        Instruments,
        db_instance,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_embedded_document(
        db_instance["stations"],
        doc_id,
        "instruments",
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Instruments])
async def create_station_instruments(
    station_instruments: Instruments,
    doc_id: str = Body(..., embed=True),
    position: Optional[int] = Body(-1, embed=True),
    db_instance=Depends(get_database),
):
    """
    API for create operation in instruments: embedded field in stations collection
    """
    station_instrument = await process_data(
        Instruments,
        db_instance,
        station_instruments.model_dump(
            exclude_unset=True, by_alias=True, exclude={"id"}
        ),
    )

    station_instrument["_id"] = bson.ObjectId()

    content = await rcu.create_embedded_document(
        db_instance["stations"],
        doc_id,
        "instruments",
        station_instrument,
        Instruments.Config.key_fields,
        position,
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=List[Instruments])
async def update_station_instrument(
    station_instrument: Instruments,
    doc_id: str = Body(..., embed=True),
    instrument_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in instruments: embedded field in stations collection
    """
    instruments = await process_data(
        Instruments,
        db_instance,
        station_instrument.model_dump(exclude={"id"}, exclude_unset=True),
    )

    content = await rcu.update_embedded_document(
        db_instance["stations"],
        {"_id": bson.ObjectId(doc_id)},
        {"_id": bson.ObjectId(instrument_id)},
        "instruments",
        instruments,
        Instruments.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_station_instruments(
    doc_id: str = Body(..., embed=True),
    instrument_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for delete operation in instruments: embedded field in stations collection
    """

    document_filter = {"_id": bson.ObjectId(doc_id)}

    content = await rcu.delete_embedded_document(
        db_instance["stations"],
        document_filter,
        {"instruments": {"_id": bson.ObjectId(instrument_id)}},
    )
    return content
