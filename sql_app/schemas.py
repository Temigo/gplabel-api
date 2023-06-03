from pydantic import BaseModel
from typing import List, Union
import datetime

# For creating annotations
class AnnotationBase(BaseModel):
    image_id: int
    x: float
    y: float
    width: float
    height: float
    label: str
    user_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

# For reading annotations
class Annotation(AnnotationBase):
    id: int

class Image(BaseModel):
    id: int
    filename: str
    frame: int = 0
    annotations: List[Annotation] = []

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

# To create user
class UserBase(BaseModel):
    email: str
    name: Union[str, None] = None
    emailVerified: Union[datetime.date, None] = None
    image: Union[str, None] = None
    annotations: List[Annotation] = []

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

# To read user
class User(UserBase):
    id: int

class ImageOut(Image):
    annotators: List[User] = []

class UserOut(User):
    images: List[Image] = []

# To create account
class AccountBase(BaseModel):
    userId: int
    type: str
    provider: str
    providerAccountId: str
    refresh_token: Union[str, None] = None
    access_token: str
    expires_at: Union[int, None] = None
    token_type: str
    scope: str
    id_token: Union[str, None] = None
    session_state: Union[str, None] = None

    class Config:
        orm_mode = True

# To read account
class Account(AccountBase):
    id: int
    user: User

# To create session
class SessionBase(BaseModel):
    expires: datetime.datetime
    sessionToken: str
    userId: int

    class Config:
        orm_mode = True

# To read session
class Session(SessionBase):
    id: int
    user: User

class VerificationToken(BaseModel):
    identifier: int
    token: str
    expires: datetime.datetime

    class Config:
        orm_mode = True
