from fastapi import APIRouter, Query
from app.services.users_service import UsersService
from app.schemas.users import UserListOut, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

service = UsersService()


@router.get("", response_model=UserListOut)
def list_users(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    return service.list_users(limit, offset)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return service.get_user(user_id)
