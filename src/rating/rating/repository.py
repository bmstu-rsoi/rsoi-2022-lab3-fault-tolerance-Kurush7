from abc import abstractmethod
from functools import reduce

import qr_server.Repository as rep


class IRatingRepository:
    @abstractmethod
    def get_rating(self, username): pass
    def set_rating(self, username): pass


class RatingRepository(IRatingRepository, rep.QRRepository):
    def __init__(self):
        super().__init__()

    def get_rating(self, username):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        rating = self.db.rating.select(self.db.rating.stars).where(username=username).one()
        return rating

    def set_rating(self, username, stars):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        ok = self.db.update(self.db.rating, auto_commit=True).set(stars=stars).where(username=username).exec()
        return ok