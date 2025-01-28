from fastapi import BackgroundTasks, APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from user.application.user_service import UserService
from typing import Annotated
from dependency_injector.wiring import inject, Provide
from containers import Container
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from common.auth import CurrentUser, get_current_user
from common.auth import get_admin_user

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    email: EmailStr = Field(max_length=64)
    password: str | None = Field(min_length=8, max_length=32, default=None)
    memo: str

class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)
    
    
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    
class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]
    

@router.post("", status_code=201, response_model=UserResponse)
@inject
def create_user(
    user:CreateUserBody,
    # background_tasks: BackgroundTasks,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    created_user = user_service.create_user(
        # background_tasks=background_tasks,
        name=user.name,
        email=user.email,
        password=user.password,
    )

    return created_user

@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    print(user_id)
    user = user_service.update_user(
        user_id=current_user.id,
        name=body.name,
        password=body.password,
    )

    return user

@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_admin_user),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> GetUsersResponse:
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count": total_count,
        "page": page,
        "users": users,
    }

    # users = user_service.get_users()
    
    # return {
    #     "users": users,
    # }

@router.post("/login")
@inject
def login(
    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    print(f"Received form data: {form_data}")
    print(f"Username: {form_data.username}, Password: {form_data.password}")    
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password,
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("", status_code=204)
@inject
def delete_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    #TODO: 다른 유저를 삭제할 수 없도록 토큰에서 유저 아이디를 구한다
    
    user_service.delete_user(current_user.id)
    
