from qr_server import parse_dict
from qr_server.dto_converter import *


def reservation_parser(d: dict):
    parse_dict(d, rename={
        'reservation_uid': 'reservationUid',
        'book_uid': 'bookUid',
        'library_uid': 'libraryUid',
        'start_date': 'startDate',
        'till_date': 'tillDate',
    },
               remove=['id', 'username'])
    d['startDate'] = d['startDate'].strftime("%Y-%m-%d")
    d['tillDate'] = d['tillDate'].strftime("%Y-%m-%d")


@dto_kwargs_parser(reservation_parser)
@dataclass
class ReservationDTO(QRDTO):
    reservationUid: str
    bookUid: str
    libraryUid: str
    status: str
    startDate: str
    tillDate: str




class ListReservationDTO(ArrayQRDTO(ReservationDTO)):
    pass
