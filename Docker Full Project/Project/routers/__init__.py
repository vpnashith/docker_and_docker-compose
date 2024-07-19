"""
    Module: __init__.py.py
    Author: Rahul George

    Description:

    License:

    Created on: 10-06-2024

"""

from fastapi import Depends
from ValidationStudioCloud.routers.login import is_token_expired

from .organisations import router as organisation
from fastapi import APIRouter
from .drivers import router as driver
from .instruments import router as instruments
from .roles import router as roles
from .roles_permissions import router as roles_permissions
from .user import router as user
from .platform_resources import router as platform_resources
from .login import router as login
from .login import get_api_key
from .instruments_category import router as instruments_category
from .instructions import router as instructions
from .instructions_arguments import router as instruction_arguments
from .instructions_responses import router as instruction_responses
from .data_transforms import router as data_transforms
from .projects import router as projects
from .facility import router as facility
from .stations import router as stations
from .stations_instruments import router as station_instruments

from .sequences import router as sequences
from .sequence_userVariables import router as sequence_user_variables
from .sequence_channels import router as sequence_channels
from .sequence_channel_groups import router as sequence_channel_groups
from .sequence_steps import router as sequence_steps

from .step_types import router as step_types
from .sequence_resources import router as resources

router = APIRouter()
router.include_router(login)
router.include_router(user)
router.include_router(
    organisation, dependencies=[Depends(is_token_expired), Depends(get_api_key)]
)
router.include_router(roles, dependencies=[Depends(is_token_expired)])
router.include_router(roles_permissions, dependencies=[Depends(is_token_expired)])
router.include_router(
    platform_resources, dependencies=[Depends(is_token_expired), Depends(get_api_key)]
)
router.include_router(instruments_category, dependencies=[Depends(is_token_expired)])
router.include_router(instruments, dependencies=[Depends(is_token_expired)])
router.include_router(driver, dependencies=[Depends(is_token_expired)])
router.include_router(instructions, dependencies=[Depends(is_token_expired)])
router.include_router(instruction_arguments, dependencies=[Depends(is_token_expired)])
router.include_router(instruction_responses, dependencies=[Depends(is_token_expired)])
router.include_router(data_transforms, dependencies=[Depends(is_token_expired)])
router.include_router(projects, dependencies=[Depends(is_token_expired)])
router.include_router(facility, dependencies=[Depends(is_token_expired)])
router.include_router(stations, dependencies=[Depends(is_token_expired)])
router.include_router(station_instruments, dependencies=[Depends(is_token_expired)])
router.include_router(sequences, dependencies=[Depends(is_token_expired)])
router.include_router(sequence_user_variables, dependencies=[Depends(is_token_expired)])
router.include_router(sequence_steps, dependencies=[Depends(is_token_expired)])
router.include_router(sequence_channel_groups, dependencies=[Depends(is_token_expired)])
router.include_router(sequence_channels, dependencies=[Depends(is_token_expired)])
router.include_router(step_types, dependencies=[Depends(is_token_expired)])
router.include_router(resources, dependencies=[Depends(is_token_expired)])
