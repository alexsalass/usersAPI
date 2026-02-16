from fastapi import HTTPException
from app.db.repositories.users_repo import UsersRepository
from app.schemas.users import UserOut, UserListOut


class UsersService:

    def __init__(self):
        self.repo = UsersRepository()

    def list_users(self, limit: int, offset: int) -> UserListOut:
        rows = self.repo.list(limit, offset)

        items = [
            UserOut(
                id=r[0],
                first_name=r[1],
                last_name=r[2],
                email=r[3],
                is_active=r[4],
                created_at=r[5],
            )
            for r in rows
        ]

        return UserListOut(count=len(items), items=items)

    def get_user(self, user_id: int) -> UserOut:
        r = self.repo.get(user_id)

        if not r:
            raise HTTPException(status_code=404, detail="User not found")

        return UserOut(
            id=r[0],
            first_name=r[1],
            last_name=r[2],
            email=r[3],
            is_active=r[4],
            created_at=r[5],
        )
