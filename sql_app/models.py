from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table, DateTime, Date
from sqlalchemy.orm import relationship, backref

from .database import Base

# Setup many-to-many relationship between users and images
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("right_id", ForeignKey("images.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
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

    images      = relationship("Image", secondary=association_table, back_populates="annotators", cascade="all")
    #annotations = relationship("Annotation", back_populates="user", cascade="all")
    #accounts    = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    #sessions    = relationship("Session", back_populates="user", cascade="all, delete-orphan")

class Image(Base):
    """

    """
    __tablename__ = "images"

    id       = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    frame    = Column(Integer)

    annotators  = relationship("User", secondary=association_table,
                                back_populates="images", cascade="all")
    #annotations = relationship("Annotation", back_populates="image", cascade="all")

class Annotation(Base):
    __tablename__ = "annotations"

    id        = Column(Integer, primary_key=True, index=True)
    image_id  = Column(Integer, ForeignKey("images.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    x         = Column(Float)
    y         = Column(Float)
    width     = Column(Float)
    height    = Column(Float)
    label     = Column(String)
    timestamp = Column(DateTime)

    image = relationship("Image", backref=backref("annotations", cascade="all"))
    user  = relationship("User", backref=backref("annotations", cascade="all"))

class Account(Base):
    """
    One-to-many relationship: one user can have multiple accounts.
    """
    __tablename__ = "accounts"

    id                = Column(Integer, primary_key=True, index=True)
    userId            = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
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

    user = relationship("User", backref=backref("accounts", cascade="all"))

class Session(Base):
    """
    One-to-many relationship: one user can have multiple sessions.
    """
    __tablename__ = "sessions"

    id           = Column(Integer, primary_key=True, index=True)
    expires      = Column(DateTime)
    sessionToken = Column(String, index=True)
    userId       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))

    user = relationship("User", backref=backref("sessions", cascade="all"))

class VerificationToken(Base):
    __tablename__ = "verificationTokens"

    identifier = Column(Integer, primary_key=True, index=True)
    token      = Column(String)
    expires    = Column(DateTime)
