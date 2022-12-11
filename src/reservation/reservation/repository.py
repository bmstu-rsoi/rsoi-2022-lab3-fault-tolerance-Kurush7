from abc import abstractmethod
from functools import reduce

import qr_server.Repository as rep


class IReservationRepository:
    @abstractmethod
    def get_reservations(self, username): pass

    @abstractmethod
    def get_reservation(self, uid): pass

    @abstractmethod
    def set_reservation_status(self, uid, status): pass

    @abstractmethod
    def create_reservation(self, res_uid, username, book_uid, library_uid,
                           status, start_date, till_date): pass

    @abstractmethod
    def delete_reservation(self, uid): pass


class ReservationRepository(IReservationRepository, rep.QRRepository):
    def __init__(self):
        super().__init__()

    def get_reservations(self, username):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        reservations = self.db.select(self.db.reservation).where(username=username).all()
        return reservations

    def get_reservation(self, uid):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        reservation = self.db.select(self.db.reservation).where(reservation_uid=uid).one()
        return reservation

    def delete_reservation(self, uid):
        ok = self.db.delete(self.db.reservation, auto_commit=True).where(reservation_uid=uid).exec()
        return ok

    def set_reservation_status(self, uid, status):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        t = self.db.reservation
        ok = self.db.update(t, auto_commit=True).set(status=status)\
            .where(reservation_uid=uid).exec()
        return ok

    def create_reservation(self, res_uid, username, book_uid, library_uid,
                           status, start_date, till_date):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')

        t = self.db.reservation
        query = t.insert(t.reservation_uid, t.username, t.book_uid, t.library_uid,
                         t.status, t.start_date, t.till_date, auto_commit=True)\
            .values([[res_uid, username, book_uid, library_uid,
                      status, start_date, till_date], ])\
            .returning(t.id, t.reservation_uid, t.username, t.book_uid, t.library_uid,
                         t.status, t.start_date, t.till_date)
        data = query.one()
        return data
