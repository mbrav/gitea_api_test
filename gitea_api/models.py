from typing import List, Optional

from pydantic import BaseModel


class NewUser(BaseModel):
    email: str
    full_name: str | None = 'Test User'
    login_name: str | None = 'test_user'
    must_change_password: bool | None = False
    password: str
    send_notify: bool | None = False
    source_id: int | None
    username: str | None = 'user'
    visibility: str | None = 'user'


if __name__ == '__main__':
    data = {
        'email': 'test@test.com',
        'password': 'asdfasdfasdf!^3453',
        'username': 'user',
    }

    user = NewUser(**data)
    print(user.dict())
