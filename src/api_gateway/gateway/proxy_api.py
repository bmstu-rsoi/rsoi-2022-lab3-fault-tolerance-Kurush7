from qr_server.Server import MethodResult, QRContext

from .dtos import *
from .utils import *
from .circuit_breaker import circuitBreaker, Service, ServiceUnavailableException


# /api/v1/libraries
@circuitBreaker.circuit([Service.LIBRARY], MethodResult('libraries not found', 503))
def list_libraries_in_city(ctx: QRContext):
    # full redirect
    address = ctx.meta['services']['library']
    resp = send_request_supress(address, 'api/v1/libraries', request=QRRequest(params=ctx.params, json_data=ctx.json_data, headers=ctx.headers))

    if resp.status_code != 200:
        raise ServiceUnavailableException(Service.LIBRARY)

    data = resp.get_json()
    return MethodResult(PagingListLibraryDTO(**data))


# /api/v1/libraries/<library_uid>/books
@circuitBreaker.circuit([Service.LIBRARY], MethodResult('books not found', 503))
def list_books_in_library(ctx: QRContext, library_uid: int):
    # full redirect
    address = ctx.meta['services']['library']
    resp = send_request_supress(address, f'api/v1/libraries/{library_uid}/books', request=QRRequest(params=ctx.params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        raise ServiceUnavailableException(Service.LIBRARY)

    data = resp.get_json()
    return MethodResult(PagingListBookDTO(**data))


# /api/v1/rating
@circuitBreaker.circuit([Service.RATING], MethodResult(ErrorDTO('Bonus Service unavailable'), 503))
def get_user_rating(ctx: QRContext):
    # full redirect
    address = ctx.meta['services']['rating']
    username = ctx.headers.environ['HTTP_X_USER_NAME']
    params = {'X-User-Name': username}
    resp = send_request_supress(address, f'api/v1/rating', request=QRRequest(params=params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        raise ServiceUnavailableException(Service.RATING)

    data = resp.get_json()
    return MethodResult(RatingDTO(**data))