from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel

from sql_app import schemas, crud
from sql_app.main import get_db
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()


@app.get("/")
def get_root():
    return {}


@app.get("/annotation/{id}", response_model=schemas.Annotation)
def get_annotation(id: int, db: Session = Depends(get_db)):
    db_anno = crud.get_annotation(db, annotation_id=id)
    if db_anno is None:
        raise HTTPException(status_code=404, detail='Annotation not found')
    return db_anno

@app.post("/annotation/new", response_model=schemas.Annotation, status_code=status.HTTP_201_CREATED)
def post_annotation(annotation: schemas.Annotation, db: Session = Depends(get_db)):
    return crud.create_annotation(db, annotation)

@app.post("/annotation/{id}/update")
def update_annotation(id: int, annotation: schemas.Annotation):
    return annotation

@app.get("/annotation/{id}/delete")
def delete_annotation(id: int):
    return { "id" : id }

@app.get("/image/{id}", response_model=schemas.ImageOut)
def get_image(id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=id)
    if db_image is None:
        raise HTTPException(status_code=404, detail='Image not found')
    return db_image

@app.get("/image/{id}/annotations", response_model=List[schemas.Annotation])
def get_image_annotations(id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=id)
    if db_image is None:
        raise HTTPException(status_code=404, detail='Image not found')
    return db_image.annotations

@app.post("/user/new", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/user/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # TODO Also return images labelled vs remaining
    db_user = crud.get_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.get("/user/{id}/images", response_model=List[schemas.ImageOut])
def get_user_images(id: int, more: bool = False, db: Session = Depends(get_db)):
    """
    more: whether to request more images at the same time.
    """
    # TODO deal with more
    db_user = crud.get_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user.images
