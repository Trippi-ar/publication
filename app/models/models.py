from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    country = Column(String, nullable=False)
    administrative_area_level_1 = Column(String, nullable=False)
    administrative_area_level_2 = Column(String)
    locality = Column(String, nullable=False)
    postal_code = Column(String)
    street = Column(String)
    street_number = Column(String)
    place_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    difficulty = Column(Integer, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    tour_guide_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    date = Column(DateTime, nullable=False)
    elevation = Column(Float)
    distance = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    details = relationship("ActivityDetails", uselist=False)

class ActivityDetails(Base):
    __tablename__ = 'activity_details'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    requirements = Column(Text)
    information = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    activity_id = Column(Integer, ForeignKey('activity.id'))


class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    image1 = Column(String)
    image2 = Column(String)
    image3 = Column(String)
    activity_id = Column(Integer, ForeignKey('activity.id'))


class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer)
    activity = Column(Integer, ForeignKey('activity.id'))


