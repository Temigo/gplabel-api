from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
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

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    images = relationship("Image", secondary=association_table, back_populates="annotators")
    annotations = relationship("Annotation", back_populates="user")

class Image(Base):
    """

    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    frame = Column(Integer)

    annotators = relationship("User", secondary=association_table, back_populates="images")
    annotations = relationship("Annotation", back_populates="image")

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    x = Column(Float)
    y = Column(Float)
    width = Column(Float)
    height = Column(Float)
    label = Column(String)
    timestamp = Column(Integer)

    image = relationship("Image", back_populates="annotations")
    user = relationship("User", back_populates="annotations")
