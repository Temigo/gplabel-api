from pydantic import BaseModel
from typing import List

class Annotation(BaseModel):
    id: int
    image_id: int
    x: float
    y: float
    width: float
    height: float
    label: str
    user_id: int
    timestamp: int

    class Config:
        orm_mode = True

class Image(BaseModel):
    id: int
    filename: str
    frame: int

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

class User(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

class ImageOut(Image):
    annotators: List[User] = []
    annotations: List[Annotation] = []

class UserOut(User):
    images: List[Image] = []
    annotations: List[Annotation] = []
