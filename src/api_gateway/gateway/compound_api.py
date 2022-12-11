from qr_server.Server import MethodResult, QRContext

from .dtos import *
from .utils import *


# /api/v1/reservations
def get_user_reservations(ctx: QRContext):
    # full redirect
    reservation_address = ctx.meta['services']['reservation']
    username = ctx.headers.environ['HTTP_X_USER_NAME']
    params = {'X-User-Name': username}

    resp = send_request(reservation_address, f'api/v1/reservations',
                        request=QRRequest(params=params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('reservations not found', 400)

    data = resp.get_json()
    book_uids = list(set([x['bookUid'] for x in data]))
    library_uids = list(set([x['libraryUid'] for x in data]))

    library_address = ctx.meta['services']['library']
    books = {uid: get_book(library_address, uid) for uid in book_uids}
    libraries = {uid: get_library(library_address, uid) for uid in library_uids}

    for d in data:
        d['book'] = books[d['bookUid']]
        d['library'] = libraries[d['libraryUid']]
        d.pop('libraryUid')
        d.pop('bookUid')

    return MethodResult(ListReservationFullDTO(data))


# /api/v1/reservations
def rent_book(ctx: QRContext):
    username = ctx.headers.environ['HTTP_X_USER_NAME']
    params = {'X-User-Name': username}

    data = ctx.json_data
    book_uid, library_uid, till_date = [data.get(x) for x in ['bookUid', 'libraryUid', 'tillDate']]

    if username is None:
        return MethodResult(RentBookError('username not found', []), 400)
    if None in [book_uid, library_uid, till_date]:
        return MethodResult(RentBookError('empty fields found', []), 400)

    reservation_address = ctx.meta['services']['reservation']
    library_address = ctx.meta['services']['library']
    rating_address = ctx.meta['services']['rating']

    # get reservations
    resp = send_request(reservation_address, f'api/v1/reservations',
                        request=QRRequest(params=params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult(RentBookError('reservations not found', []), 400)
    reservations = resp.get_json()

    # get user rating
    resp = send_request(rating_address, f'api/v1/rating',
                        request=QRRequest(params=params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('user not found', 400)
    rating = resp.get_json()

    if len(reservations) >= rating['stars']:
        return MethodResult(RentBookError('reservations limit reached', []), 400)

    # decrease library
    resp = send_request(library_address, f'api/v1/libraries/{library_uid}/books/{book_uid}/rent', method='POST',
                        request=QRRequest())
    if resp.status_code != 200:
        return MethodResult('can\'t rent book from library', 400)

    # create reservation
    resp = send_request(reservation_address, f'api/v1/reservations', method='POST',
                        request=QRRequest(json_data={'username': username, 'library_uid': library_uid,
                                                     'book_uid': book_uid, 'till_date': till_date}))
    if resp.status_code != 200:
        return MethodResult('can\'t create reservation', 400)
        # todo release book
    reservation = resp.get_json()
    _expand_reservation(reservation, library_address)

    reservation['rating'] = rating
    return MethodResult(CreateReservationDTO(**reservation))


# /api/v1/reservations/<reservation_uid>/return
def return_book(ctx: QRContext, reservation_uid: str):
    username = ctx.headers.environ['HTTP_X_USER_NAME']
    params = {'X-User-Name': username}

    data = ctx.json_data
    condition, date = [data.get(x) for x in ['condition', 'date']]

    if username is None:
        return MethodResult(ReturnBookError('username not found'), 400)
    if None in [condition, date]:
        return MethodResult(ReturnBookError('empty fields found'), 400)

    reservation_address = ctx.meta['services']['reservation']
    library_address = ctx.meta['services']['library']
    rating_address = ctx.meta['services']['rating']

    # get reservation
    resp = send_request(reservation_address, f'api/v1/reservations/{reservation_uid}', request=QRRequest())
    if resp.status_code != 200:
        return MethodResult('reservation not found', 400)
    reservation = resp.get_json()
    status = reservation['status']
    if status != 'RENTED':
        return MethodResult(ReturnBookError('reservation\'s status is not RENTED'), 400)

    library_uid, book_uid, till_date = reservation['libraryUid'], reservation['bookUid'], reservation['tillDate']

    # get user rating
    resp = send_request(rating_address, f'api/v1/rating',
                        request=QRRequest(params=params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('user not found', 400)
    rating = resp.get_json()

    # get book condition
    resp = send_request(library_address, f'api/v1/books/{book_uid}', request=QRRequest())
    if resp.status_code != 200:
        return MethodResult('book not found', 400)
    book = resp.get_json()
    book_pre_condition = book['condition']

    # return book: library
    # note: what if condition has worsened?
    resp = send_request(library_address, f'api/v1/libraries/{library_uid}/books/{book_uid}/return', method='POST',
                        request=QRRequest())
    if resp.status_code != 200:
        return MethodResult('can\'t return book to library', 400)

    # update rating
    new_stars = rating['stars']
    ok = True
    date, till_date = datetime.strptime(date, "%Y-%m-%d"), datetime.strptime(till_date, "%Y-%m-%d")
    if date > till_date:
        ok = False
        new_stars -= 10
    if _condition_worsened(book_pre_condition, condition):
        ok = False
        new_stars -= 10
    if ok:
        new_stars += 1

    params['stars'] = new_stars
    resp = send_request(rating_address, f'api/v1/rating',
                        request=QRRequest(params=params), method='PUT')
    if resp.status_code != 200:
        return MethodResult('can\'t update rating', 400)

    # update reservation status
    res_status = 'EXPIRED' if (date > till_date) else 'RETURNED'
    resp = send_request(reservation_address, f'api/v1/reservations/{reservation_uid}', method='POST',
                        request=QRRequest(params={'status': res_status}))
    if resp.status_code != 200:
        return MethodResult('reservation status not updated', 400)

    return MethodResult(status_code=204)


def _expand_reservation(res, library_address):
    book_uid = res['bookUid']
    library_uid = res['libraryUid']

    book = get_book(library_address, book_uid)
    library = get_library(library_address, library_uid)

    res['book'] = book
    res['library'] = library
    res.pop('libraryUid')
    res.pop('bookUid')


def _condition_worsened(prev, cur):
    if prev == 'EXCELLENT':
        return cur != 'EXCELLENT'
    elif prev == 'GOOD':
        return cur not in ['EXCELLENT', 'GOOD']
    elif prev == 'BAD':
        return False
    else:
        raise Exception(f'unknown book condition {prev}')
