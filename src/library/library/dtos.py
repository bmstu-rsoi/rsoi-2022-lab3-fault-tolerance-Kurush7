from typing import Dict

from qr_server.dto_converter import *
from qr_server.dict_parsing import *


def library_parser(d: dict):
    parse_dict(d, rename={'library_uid': 'libraryUid'}, remove=['id'])


def book_parser(d: dict):
    parse_dict(d, rename={'book_uid': 'bookUid', 'available_count': 'availableCount'}, remove=['id'])

def uncounted_book_parser(d: dict):
    parse_dict(d, rename={'book_uid': 'bookUid'},
               remove=['id',])

def short_book_parser(d: dict):
    parse_dict(d, rename={'book_uid': 'bookUid', 'available_count': 'availableCount'},
               remove=['id', 'condition'])


@dataclass
class BookDummyDTO(QRDTO):
    bookUid: str

@dataclass
class LibraryDummyDTO(QRDTO):
    bookUid: str

@dto_kwargs_parser(library_parser)
@dataclass
class LibraryDTO(QRDTO):
    libraryUid: str
    name: str
    address: str
    city: str


@dto_kwargs_parser(book_parser)
@dataclass
class BookDTO(QRDTO):
    bookUid: str
    name: str
    author: str
    genre: str
    condition: str
    availableCount: str

@dto_kwargs_parser(uncounted_book_parser)
@dataclass
class UncountedBookDTO(QRDTO):
    bookUid: str
    name: str
    author: str
    genre: str
    condition: str


@dto_kwargs_parser(short_book_parser)
@dataclass
class BookShortDTO(QRDTO):
    bookUid: str
    name: str
    author: str
    genre: str


@dataclass
class PagingList(QRDTO):
    page: int
    pageSize: int
    totalElements: int
    items: List[Dict]


@convert_fields({'[]items': LibraryDTO, })
class PagingListLibraryDTO(PagingList):
    pass


@convert_fields({'[]items': BookDTO, })
class PagingListBookDTO(PagingList):
    pass
