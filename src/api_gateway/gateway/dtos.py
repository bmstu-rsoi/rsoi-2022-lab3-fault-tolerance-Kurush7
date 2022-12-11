import sys
sys.path.append('..')

from rating.rating.dtos import *
from library.library.dtos import *
from reservation.reservation.dtos import *

@dataclass
class ReservationFullDTO(QRDTO):
    reservationUid: str
    book: BookShortDTO
    library: LibraryDTO
    status: str
    startDate: str
    tillDate: str

@dataclass
class ReservationDummyDTO(QRDTO):
    reservationUid: str
    book: BookDummyDTO
    library: LibraryDummyDTO
    status: str
    startDate: str
    tillDate: str


@dataclass
class RequestError(QRDTO):
    field: str
    error: str


@convert_fields({'[]errors': RequestError})
@dataclass
class RentBookError(QRDTO):
    message: str
    errors: List[Dict]


@dataclass
class ReturnBookError(QRDTO):
    message: str

@dataclass
class ErrorDTO(QRDTO):
    message: str


@dataclass
class CreateReservationDTO(ReservationFullDTO):
    rating: RatingDTO


class ListReservationFullDTO(ArrayQRDTO(ReservationFullDTO)):
    pass

class ListReservationDummyDTO(ArrayQRDTO(ReservationDummyDTO)):
    pass
