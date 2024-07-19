# flake8: noqa: D209,D210,D400,D415,I001
""" Module: data_transforms

Author: Neethukrishnan P

Description:

License:

Created on: 07-03-2024 """

import os
from datetime import datetime
from typing import List
from fastapi import APIRouter, Body, Depends, status, UploadFile
import bson
from ValidationStudioCloud.dependencies import get_database
from ValidationStudioCloud.models.data_transforms import DataTransform
from ValidationStudioCloud.settings import settings
from ValidationStudioCloud.utils.exceptions import (
    ValidationStudioError,
    ErrorCodes,
)
from ValidationStudioCloud.utils import rest_controller_utils as rcu
from ValidationStudioCloud.utils.rest_utils import FilterModel
from ValidationStudioCloud.utils.utils import (
    convert_str_id_to_object_id,
    process_data,
)

router = APIRouter(prefix="/data_transforms", tags=["data_transforms"])


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=List[DataTransform.FilterBy],
    response_model_exclude_unset=True,
)
async def search_data_transforms(
    filter_model: FilterModel[DataTransform.FilterBy, DataTransform.Unset],
    db_instance=Depends(get_database),  # noqa: B008
):
    """API for search operation data_transforms"""  # noqa: D400, D401, D415
    filter_by_dict = convert_str_id_to_object_id(
        DataTransform,
        filter_model.filter_by.model_dump(exclude_unset=True, by_alias=True),
    )

    return await rcu.read_documents(
        db_instance["data_transforms"],
        filter_by_dict,
        filter_model.unset.model_dump(exclude_unset=True, by_alias=True),
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=List[DataTransform]
)  # noqa: B008
async def create_data_transforms(
    data_transform: DataTransform,
    db_instance=Depends(get_database),  # noqa: D400, D401, D415, B008
):
    """API for create operation for data transform."""  # noqa: D401
    # noqa: D202, D400, D401, D415
    data_transform = await process_data(
        DataTransform, db_instance, data_transform.model_dump(exclude={"id"})
    )
    data_transform["created_on"] = datetime.now()

    return rcu.create_document(
        db_instance["data_transforms"], data_transform, DataTransform.Config.key_fields
    )


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=DataTransform)
async def update_data_transforms(
    data_transform: DataTransform.FilterBy,
    doc_id: str = Body(..., embed=True),
    db_instance=Depends(get_database),  # noqa: D400, B008
):
    """API for update operation in data_transforms."""  # noqa: D401, D415
    # noqa: B008, D202, D400
    data_transforms = await process_data(
        DataTransform,
        db_instance,
        data_transform.model_dump(exclude={"id"}, exclude_unset=True),
    )

    # on update of is_deleted
    if "is_deleted" in data_transforms and "deleted_by" not in data_transforms:
        raise ValidationStudioError(
            ErrorCodes.MANDATORY_FIELD_MISSING,
            ("routers", "update"),
            detail="deleted_by field should be given "
            "when is_deleted is updating into true",
        )

    data_transforms["last_updated"] = datetime.now()

    return await rcu.update_document(
        db_instance["data_transforms"],
        bson.ObjectId(doc_id),
        data_transforms,
        DataTransform.Config.key_fields,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_transforms(
    doc_id: str = Body(..., embed=True), db_instance=Depends(get_database)  # noqa: B008
):
    """API for delete operation in data_transforms collection"""  # noqa: D415, D202, D400, D401

    return await rcu.delete_document(
        db_instance["data_transforms"], bson.ObjectId(doc_id)
    )


@router.post("/file_upload", status_code=status.HTTP_200_OK)
async def data_transform_file_upload(
    file: UploadFile,
    name: str = Body(...),
    db_instance=Depends(get_database),  # noqa: B008
):
    """File Upload endpoint for data_transform"""  # noqa: D415, D400
    data_transform_path = str(settings.DATA_TRANSFORM_PATH)
    os.makedirs(data_transform_path, exist_ok=True)

    try:
        file_location = os.path.join(data_transform_path, file.filename).replace(
            "\\", "/"
        )
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        file_location = "ValidationStudioCloud" + "/" + file_location

        document = await rcu.read_documents(
            db_instance["data_transforms"], {"name": name}, {}
        )
        if document:
            await rcu.update_document(
                db_instance["data_transforms"],
                document[0]["_id"],
                {"file_path": file_location},
                set(),
            )
        else:
            raise ValidationStudioError(
                error_code=ErrorCodes.DOCUMENT_NOT_FOUND,
                location=("routers", "data_transforms", "file_upload"),
                detail="document_Search",
            )
    except Exception as e:
        raise ValidationStudioError(  # noqa: B904
            error_code=ErrorCodes.MODIFY_DOCUMENT_FAILED,
            location=("routers", "data_transforms", "file_upload"),
            detail=e,
        )

    return "upload success"
