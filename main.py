from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sql_app import schemas, crud
from sql_app.main import get_db
from sqlalchemy.orm import Session
from typing import List

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("foo")
log.debug("test")

app = FastAPI(
    title="GP Label API",
    version="0.0.1"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_root():
    return {}

#
# Annotation routes
#

@app.get("/annotation/{id}", response_model=schemas.Annotation)
def get_annotation(id: int, db: Session = Depends(get_db)):
    db_anno = crud.get_annotation(db, annotation_id=id)
    if db_anno is None:
        raise HTTPException(status_code=404, detail='Annotation not found')
    return db_anno

@app.post("/annotation/new", response_model=schemas.Annotation, status_code=status.HTTP_201_CREATED)
def post_annotation(annotation: schemas.AnnotationBase, db: Session = Depends(get_db)):
    return crud.create_annotation(db, annotation)

@app.post("/annotation/{id}/update")
def update_annotation(id: int, annotation: schemas.Annotation):
    return annotation

@app.post("/annotation/{id}/delete")
def delete_annotation(id: int):
    return { "id" : id }

#
# Image routes
#

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

#
# User routes
#

@app.post("/user/new", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/user/update", response_model=schemas.UserOut)
def update_user(user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(db, user)

@app.get("/user/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # TODO Also return images labelled vs remaining
    db_user = crud.get_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.get("/user/email/", response_model=schemas.UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.get("/user/account/", response_model=schemas.UserOut)
def get_user_by_account(provider_account_id: str, provider: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_account(db, provider_account_id, provider)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.get("/user/{id}/images/", response_model=List[schemas.ImageOut])
def get_user_images(id: int, more: bool = False, db: Session = Depends(get_db)):
    """
    more: whether to request more images at the same time.
    """
    # TODO deal with more
    db_user = crud.get_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user.images

@app.post("/account/new", response_model=schemas.Account)
def create_account(account: schemas.AccountBase, db: Session = Depends(get_db)):
    return crud.create_account(db, account)

@app.post("/session/new", response_model=schemas.Session)
def create_session(session: schemas.SessionBase, db: Session = Depends(get_db)):
    return crud.create_session(db, session)

@app.get("/session/{token}", response_model=schemas.Session)
def get_session_and_user(token: str, db: Session = Depends(get_db)):
    return crud.get_session_and_user(db, token)

@app.post("/session/update", response_model=schemas.Session)
def update_session(session: schemas.Session, db: Session = Depends(get_db)):
    return crud.update_session(db, session)

@app.post("/session/delete/", response_model=schemas.SessionBase)
def delete_session(sessionToken: str, db: Session = Depends(get_db)):
    log.debug(sessionToken)
    s = crud.delete_session(db, sessionToken)
    log.debug(s)
    return s

@app.post("/verificationToken/new", response_model=schemas.VerificationToken)
def create_verification_token(token: schemas.VerificationToken, db: Session = Depends(get_db)):
    return crud.create_verification_token(db, token)

@app.post("/verificationToken/use", response_model=schemas.VerificationToken)
def use_verification_token(token: schemas.VerificationToken, db: Session = Depends(get_db)):
    return crud.use_verification_token(db, token)
