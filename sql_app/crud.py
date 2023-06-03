from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def get_annotation(db: Session, annotation_id: int):
    return db.query(models.Annotation).filter(models.Annotation.id == annotation_id).first()

def create_annotation(db: Session, annotation: schemas.Annotation):
    db_anno = models.Annotation(**annotation.dict())
    db.add(db_anno)
    db.commit()
    db.refresh(db_anno)
    return db_anno
