import sys
sys.path.append("..")
sys.path.append("../common")

import datetime
import uuid

from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer

from reservation.repository import ReservationRepository
from reservation.dtos import *
from common.common_api import health


def get_user_reservations(ctx: QRContext):
    username = ctx.params.get('X-User-Name')

    reservations = ctx.repository.get_reservations(username)
    if reservations is None:
        return MethodResult('user not found', 400)
    return MethodResult(ListReservationDTO(reservations))


def create_reservation(ctx: QRContext):
    data = ctx.json_data
    username, book_uid, library_uid, till_date = [data.get(x) for x in ['username', 'book_uid', 'library_uid', 'till_date']]
    if None in [username, book_uid, library_uid, till_date]:
        return MethodResult('bad parameters', 400)

    res_uid = str(uuid.uuid4())
    status = 'RENTED'
    start_date = datetime.datetime.now()

    reservation = ctx.repository.create_reservation(res_uid, username, book_uid, library_uid,
                                                     status, start_date, till_date)
    if reservation is None:
        return MethodResult('user not found', 400)
    return MethodResult(ReservationDTO(**reservation))


def delete_reservation(ctx: QRContext, reservation_uid):
    reservation = ctx.repository.delete_reservation(reservation_uid)
    if reservation is None:
        return MethodResult('failed to delete reservation', 400)
    return MethodResult()


def get_reservation(ctx: QRContext, reservation_uid):
    reservation = ctx.repository.get_reservation(reservation_uid)
    if reservation is None:
        return MethodResult('reservation not found', 400)
    return MethodResult(ReservationDTO(**reservation))

def set_reservation_status(ctx: QRContext, reservation_uid):
    status = ctx.params.get('status')
    ok = ctx.repository.set_reservation_status(reservation_uid, status)
    if not ok:
        return MethodResult('can\'t update reservation status', 400)
    return MethodResult()


class ReservationServer(FlaskServer, ReservationRepository):
    def __init__(self):
        super().__init__(400)


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    server = ReservationServer()
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])
        server.logger.info(f'repository: found tables: {[x for x in server.db.meta["tables"]]}')

    server.register_method('/api/v1/reservations', get_user_reservations, 'GET')
    server.register_method('/api/v1/reservations/<reservation_uid>', get_reservation, 'GET')
    server.register_method('/api/v1/reservations', create_reservation, 'POST')
    server.register_method('/api/v1/reservations/<reservation_uid>', delete_reservation, 'DELETE')
    server.register_method('/api/v1/reservations/<reservation_uid>', set_reservation_status, 'POST')
    server.register_method('/manage/health', health, 'GET')
    server.run(host, port)
