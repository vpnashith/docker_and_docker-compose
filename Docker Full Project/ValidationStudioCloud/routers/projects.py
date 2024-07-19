"""
    Module: projects.py

    Author: Rithwik

    Description: route for projects

    License:

    Created on: 02-07-2024

"""

from typing import List
from datetime import datetime
import bson
from fastapi import APIRouter, Body, Depends, status

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.projects import Project
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import convert_str_id_to_object_id, process_data, soft_delete_pre_check
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    ErrorCodes,
    MongoError,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[Project.FilterBy],
    response_model_exclude_unset=True,
)
async def search_projects(
    filter_model: FilterModel[Project.FilterBy, Project.Unset],
    db_instance=Depends(get_database),
):
    """
    API for search operation in projects collection
    """

    filter_by_dict = convert_str_id_to_object_id(
        Project,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    content = await rcu.read_documents(
        db_instance["projects"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )
    return content


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Project])
async def create_projects(project: Project, db_instance=Depends(get_database)):
    """
    API for create operation in project collection
    """

    try:
        project = await process_data(
            Project, db_instance, project.model_dump(exclude={"id", "is_deleted"})
        )
    except MongoError as e:
        raise ValidationStudioError(
            error_code=e.error_code,
            location=("instruction", "create"),
            detail="Foreign key check failed",
        )

    project["created_on"], project["last_updated"] = (
        datetime.now(),
        datetime.now(),
    )

    content = await rcu.create_document(
        db_instance["projects"], project, Project.Config.key_fields
    )

    return content


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Project)
async def update_projects(
    project: Project.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),
):
    """
    API for update operation in project collection
    """
    project = await process_data(
        Project,
        db_instance,
        project.model_dump(exclude={"id", "created_on", "created_by"}, exclude_unset=True),
    )

    project["last_updated"] = datetime.now()
    await soft_delete_pre_check(doc_id, project, db_instance, "projects")
    content = await rcu.update_document(
        db_instance["projects"],
        bson.ObjectId(doc_id),
        project,
        Project.Config.key_fields,
    )
    return content


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_projects(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)
):
    """
    API for delete operation in project collection
    """

    content = await rcu.delete_document(db_instance["projects"], bson.ObjectId(doc_id))
    return content
