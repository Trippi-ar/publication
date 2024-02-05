import uuid

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime


Base = declarative_base()


class TimestampedUUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Address(Base, TimestampedUUIDMixin):
    __tablename__ = 'address'

    country = Column(String, nullable=False)
    administrative_area_level_1 = Column(String, nullable=False)
    administrative_area_level_2 = Column(String)
    locality = Column(String, nullable=False)
    place_id = Column(String, unique=True)
    full_address = Column(String, nullable=False)


class Publication(Base, TimestampedUUIDMixin):
    __tablename__ = 'publication'

    address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'))
    # agregar address
    tour_guide_id = Column(UUID(as_uuid=True), nullable=False)
    languages = relationship("Languages", back_populates="publication")
    images = relationship("Images", back_populates="publication")
    activity = relationship("Activity", back_populates="publication")

    name = Column(String, nullable=False, unique=True)
    difficulty = Column(String, nullable=False)
    distance = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    tools = Column(Text, nullable=False)
    type = Column(String, nullable=False)


class Languages(Base, TimestampedUUIDMixin):
    __tablename__ = 'languages'

    publication_id = Column(UUID(as_uuid=True), ForeignKey('publication.id'))
    publication = relationship("Publication", back_populates="languages")

    language = Column(Enum('spanish', 'english', 'french', name='Languages'), nullable=False)


class Images(Base, TimestampedUUIDMixin):
    __tablename__ = 'images'

    publication_id = Column(UUID(as_uuid=True), ForeignKey('publication.id'))
    publication = relationship("Publication", back_populates="images")

    image_url = Column(String, nullable=False, unique=True)


class Activity(Base, TimestampedUUIDMixin):
    __tablename__ = 'activity'

    publication_id = Column(UUID(as_uuid=True), ForeignKey('publication.id'))
    publication = relationship("Publication", back_populates="activity")
    bookings = relationship("Booking", back_populates="activity")

    date = Column(DateTime, nullable=False)
    max_participants = Column(Integer, nullable=False)
    available_spots = Column(Integer, nullable=False)
    is_full = Column(Boolean, default=False, nullable=False)

    def update_is_full(self):
        self.is_full = self.available_spots <= 0

    def reserve_spot(self, quantity=1):
        if self.available_spots is None or self.available_spots >= quantity:
            self.available_spots = max(0, self.available_spots - quantity)
            self.update_is_full()

    def cancel_spot(self, quantity=1):
        if self.available_spots is None:
            self.available_spots = self.max_participants - quantity
        else:
            self.available_spots = min(self.max_participants, self.available_spots + quantity)
        self.update_is_full()


class Booking(Base, TimestampedUUIDMixin):
    __tablename__ = 'booking'

    activity_id = Column(UUID(as_uuid=True), ForeignKey('activity.id'))
    user_id = Column(UUID(as_uuid=True), nullable=False)
    activity = relationship("Activity", back_populates="bookings")

    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    state = Column(Enum('pending', 'confirmed', 'cancelled', name='booking_state'), default='pending', nullable=False)
