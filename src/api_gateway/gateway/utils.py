from enum import Enum

from qr_server.request_sending import *


class Service(Enum):
    LIBRARY = 1
    RATING = 2
    RESERVATION = 3


def get_book(address: QRAddress, uid: str):
    resp = send_request_supress(address, f'api/v1/books/{uid}')
    if resp.status_code != 200:
        return None
    return resp.get_json()


def get_library(address: QRAddress, uid: str):
    resp = send_request_supress(address, f'api/v1/libraries/{uid}')
    if resp.status_code != 200:
        return None
    return resp.get_json()


def send_request_supress(address: QRAddress, url: str, method='GET', request: QRRequest = None):
    try:
        return send_request(address, url, method, request)
    except Exception as e:
        return QRResponse(False, 500, str(e), bytes())


def knock_service(address: QRAddress, throw_exception: bool = False):
    try:
        resp = requests.request('GET', address.get_full_url('manage/health'))
        ok = resp.status_code == 200
    except Exception:
        ok = False
    if throw_exception and not ok:
        raise Exception('knock service: failed')
    return ok