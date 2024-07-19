"""
    Module: login.py
    Author: Radhika Krishnan

    Description: Router for the Login

    License:

    Created on: 02-07-2024

"""

import ValidationStudioCloud.utils.rest_controller_utils as rcu
from fastapi import Depends, HTTPException, status, APIRouter, Header
from fastapi.security import APIKeyHeader
from ValidationStudioCloud.dependencies import get_database
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt


SECRET_KEY = "498d6919122fa8c9e851558b041b5bd56238023bc7f4b7670f9bdec6f8b8f158"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


API_KEY_NAME = "X-VSC-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_req_header: str = Depends(api_key_header)):
    if api_key_req_header == SECRET_KEY:
        return api_key_req_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )


router = APIRouter(tags=["Login"])


async def get_user_from_db(db_instance, email):
    """Function to get the email and password from the users collection"""
    content = await rcu.read_documents(
        db_instance["users"],
        filter_by={"email": email},
        projection={"email": 1, "password": 1, "role_id": 1},
    )
    return content


def verify_password(plain_password, hashed_password):
    """Function to verify the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Function to hash the password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Function to create access token and return the JWT token"""
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"expire": str(expire)})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def is_token_expired(token: str = Header(...)):
    """Function to check whether the token is expired or not"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    payload["expire"] = datetime.strptime(payload["expire"], "%Y-%m-%d %H:%M:%S.%f")
    if datetime.now() > payload["expire"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="expired token"
        )


@router.post("/login")
async def login(email: str, password: str, db_instance=Depends(get_database)):
    current_user = await get_user_from_db(db_instance, email)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not Exist"
        )
    if not verify_password(password, str(current_user[0]["password"])):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password"
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    user_id = current_user[0]["_id"]
    role_id = current_user[0]["role_id"]

    # Get the role content from the roles collection
    role_content = await rcu.read_documents(
        db_instance["roles"],
        filter_by={"_id": role_id},
        projection={"permissions": 1},
    )
    roles_permission = []
    role_permission = role_content[0]

    permissions = role_permission.get("permissions", {})
    for ele in permissions:
        platform_resource_id = ele["platform_resource_id"]
        # Get the corresponding platform resource document
        platform_resource = await rcu.read_documents(
            db_instance["platform_resources"],
            filter_by={"_id": platform_resource_id},
            projection={"name": 1},
        )
        if platform_resource:
            result = {}
            result[platform_resource[0]["name"]] = ele["given_permissions"]
            roles_permission.append(result)

    print("role", roles_permission)

    access_token = create_access_token(
        data={
            "user_id": str(user_id),
            "sub": current_user[0]["email"],
            "roles_permission": roles_permission,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
