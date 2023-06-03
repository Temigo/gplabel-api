from sqlalchemy.orm import Session

from . import models, schemas

#
# User
#
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_user_by_account(db: Session, provider_account_id: str, provider: str):
    account = db.query(models.Account).filter(
        (models.Account.provider == provider) and (models.Account.providerAccountId == provider_account_id)
    ).first()
    if account is not None:
        return account.user
    else:
        return None

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.User):
    db.update(user, synchronize_session = False)
    db.commit()
    db.refresh(user)
    return user

#
# Image
#
def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

#
# Annotation
#
def get_annotation(db: Session, annotation_id: int):
    return db.query(models.Annotation).filter(models.Annotation.id == annotation_id).first()

def create_annotation(db: Session, annotation: schemas.AnnotationBase):
    db_anno = models.Annotation(**annotation.dict())
    db.add(db_anno)
    db.commit()
    db.refresh(db_anno)
    return db_anno

#
# Account
#
def create_account(db: Session, account: schemas.AccountBase):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

#
# Session
#
def create_session(db: Session, session: schemas.SessionBase):
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session_and_user(db: Session, token: str):
    return db.query(models.Session).filter(models.Session.sessionToken == token).first()

def update_session(db: Session, session: schemas.Session):
    db.update(session, synchronize_session = False)
    db.commit()
    db.refresh(session)
    return session

def delete_session(db: Session, sessionToken: str):
    db_session = db.query(models.Session).filter(models.Session.sessionToken == sessionToken).one()
    session = schemas.SessionBase(**db_session._asdict())
    db.delete(db_session)
    db.commit()
    return session

#
# VerificationToken
#
def create_verification_token(db: Session, token: schemas.VerificationToken):
    db_token = models.VerificationToken(**token.dict())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

# FIXME the token here does not necessarily have expire?
def use_verification_token(db: Session, token: schemas.VerificationToken):
    db_token = db.query(models.VerificationToken).filter(
        (models.VerificationToken.identifier == token.identifier) and (models.VerificationToken.token == token.token)
    ).first()
    token = schemas.VerificationToken(**db_token._asdict())
    db.delete(db_token)
    db.commit()
    return token
