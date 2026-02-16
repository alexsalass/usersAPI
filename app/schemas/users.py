from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: Optional[datetime]


class UserListOut(BaseModel):
    count: int
    items: List[UserOut]
