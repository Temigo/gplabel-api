from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table, DateTime, Date
from sqlalchemy.orm import relationship

from .database import Base

# Setup many-to-many relationship between users and images
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("users.id"), primary_key=True),
    Column("right_id", ForeignKey("images.id"), primary_key=True)
)

class User(Base):
    """
    One-to-many relationship with annotations
    Many-to-many relationship with images
    """
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    email         = Column(String, unique=True, index=True)
    name          = Column(String)
    emailVerified = Column(Date)
    image         = Column(String)

    images      = relationship("Image", secondary=association_table, back_populates="annotators")
    annotations = relationship("Annotation", back_populates="user")
    accounts    = relationship("Account", back_populates="user")
    sessions    = relationship("Session", back_populates="user")

class Image(Base):
    """

    """
    __tablename__ = "images"

    id       = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    frame    = Column(Integer)

    annotators  = relationship("User", secondary=association_table, back_populates="images")
    annotations = relationship("Annotation", back_populates="image")

class Annotation(Base):
    __tablename__ = "annotations"

    id        = Column(Integer, primary_key=True, index=True)
    image_id  = Column(Integer, ForeignKey("images.id"))
    user_id   = Column(Integer, ForeignKey("users.id"))
    x         = Column(Float)
    y         = Column(Float)
    width     = Column(Float)
    height    = Column(Float)
    label     = Column(String)
    timestamp = Column(DateTime)

    image = relationship("Image", back_populates="annotations")
    user  = relationship("User", back_populates="annotations")

class Account(Base):
    """
    One-to-many relationship: one user can have multiple accounts.
    """
    __tablename__ = "accounts"

    id                = Column(Integer, primary_key=True, index=True)
    userId            = Column(Integer, ForeignKey("users.id"))
    type              = Column(String)
    provider          = Column(String)
    providerAccountId = Column(String)
    refresh_token     = Column(String)
    access_token      = Column(String)
    expires_at        = Column(Integer)
    token_type        = Column(String)
    scope             = Column(String)
    id_token          = Column(String)
    session_state     = Column(String)

    user = relationship("User", back_populates="accounts")

class Session(Base):
    """
    One-to-many relationship: one user can have multiple sessions.
    """
    __tablename__ = "sessions"

    id           = Column(Integer, primary_key=True, index=True)
    expires      = Column(Date)
    sessionToken = Column(String, index=True)
    userId       = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="sessions")

class VerificationToken(Base):
    __tablename__ = "verificationTokens"

    identifier = Column(Integer, primary_key=True, index=True)
    token      = Column(String)
    expires    = Column(DateTime)
