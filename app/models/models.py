from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
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
    is_active = Column(Boolean, default=True)


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
    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    languages = Column(String, nullable=False)
    transport = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    tools = Column(Text, nullable=False)
    itinerary = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    type = Column(String, nullable=False)


class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    image = Column(String)
    description = Column(String)
    activity_id = Column(Integer, ForeignKey('activity.id'))


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    user_id = Column(Integer, nullable=False)
    number_people = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    state = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
