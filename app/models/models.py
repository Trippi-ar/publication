import uuid

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class TimestampedUUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True)


class Address(Base, TimestampedUUIDMixin):
    __tablename__ = 'address'

    country = Column(String, nullable=False)
    administrative_area_level_1 = Column(String, nullable=False)
    administrative_area_level_2 = Column(String)
    locality = Column(String, nullable=False)
    place_id = Column(String, unique=True)


class Publication(Base, TimestampedUUIDMixin):
    __tablename__ = 'publication'

    address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'))
    tour_guide_id = Column(UUID(as_uuid=True), nullable=False)
    languages = relationship("PublicationLanguages", back_populates="publication")
    images = relationship("Images", back_populates="publication")

    
    name = Column(String, nullable=False, unique=True)
    difficulty = Column(Enum('1', '2', '3', '4', '5'), nullable=False)
    distance = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    tools = Column(Text, nullable=False)
    type = Column(String, nullable=False)


class PublicationLanguages(Base, TimestampedUUIDMixin):
    __tablename__ = 'publication_languages'

    publication_id = Column(UUID(as_uuid=True), ForeignKey('publication.id'))
    publication = relationship("Publication", back_populates="languages")

    
    language = Column(Enum('spanish', 'english', 'french','mandarin','portuguese'), nullable=False)


class Images(Base, TimestampedUUIDMixin):
    __tablename__ = 'images'

    publication_id = Column(UUID(as_uuid=True), ForeignKey('publication.id'))
    publication = relationship("Publication", back_populates="images")


    image_url = Column(String, nullable=False)


class Activity(Base, TimestampedUUIDMixin):
    __tablename__ = 'activity'

    dates = relationship("ActivityDates", back_populates="activity")
    bookings = relationship("Booking", back_populates="activity")




class ActivityDates(Base, TimestampMixin):
    __tablename__ = 'activity_dates'

    activity_id = Column(UUID(as_uuid=True), ForeignKey('activity.id'))
    activity = relationship("Activity", back_populates="dates")

    
    date = Column(DateTime, nullable=False)


class Booking(Base, TimestampMixin):
    __tablename__ = 'booking'

    activity_id = Column(UUID(as_uuid=True), ForeignKey('activity.id'))         
    user_id = Column(UUID(as_uuid=True), nullable=False)
    activity = relationship("Activity", back_populates="bookings")


    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    state = Column(Enum('pending', 'confirmed', 'cancelled', name='booking_state'), nullable=False)