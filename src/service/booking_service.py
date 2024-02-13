from fastapi import HTTPException, status

from src.repository.booking_repository import BookingRepository
from src.schema import booking_schema

from src.utils import errors
from src.utils.utils import authenticate

repository = BookingRepository()


class BookingService:
    @staticmethod
    def create(create_booking: booking_schema.Request, token):
        try:
            # authentication = authenticate(token.credentials, 'client')
            authentication = authenticate(token.credentials, 'guide')
            return repository.create(booking_schema.Create(
                publication_id=create_booking.publication_id,
                user_id=authentication.get('user_id'),
                participant=create_booking.participant,
                date=create_booking.date,
            ))
        except errors.AuthenticationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Booking failed")

    @staticmethod
    def get_all(token):
        try:
            # authentication = authenticate(token.credentials, 'client')
            authentication = authenticate(token.credentials, 'public')
            if authentication.get('role') == 'guide':
                return repository.get_all(authentication.get('user_id'))
            else:
                return repository.get_all_guide(authentication.get('user_id'))
        except errors.AuthenticationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Get bookings failed")

    @staticmethod
    def check_availability(availability: booking_schema.Availability):
        try:
            return repository.check_availability(availability)
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Availability check failed")

    @staticmethod
    def update(booking_id, update_booking: booking_schema.Update, token):
        try:
            authentication = authenticate(token.credentials, 'client')
            return repository.update(booking_id, update_booking)
        except errors.AuthenticationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Update booking failed")