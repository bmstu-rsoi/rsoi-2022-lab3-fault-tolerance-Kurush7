import sys
sys.path.append("..")
sys.path.append("../common")

from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer

from rating.repository import RatingRepository
from rating.dtos import *
from common.common_api import health


def get_user_rating(ctx: QRContext):
    username = ctx.params.get('X-User-Name')

    rating = ctx.repository.get_rating(username)
    if rating is None:
        return MethodResult('user not found', 400)
    return MethodResult(RatingDTO(**rating))


def set_user_rating(ctx: QRContext):
    username = ctx.params.get('X-User-Name')
    stars = ctx.params.get('stars')

    if None in [stars, username]:
        raise Exception('username or stars fields are missing')

    ok = ctx.repository.set_rating(username, stars)
    if not ok:
        return MethodResult('can\'t update rating', 400)
    return MethodResult('ok')


class RatingServer(FlaskServer, RatingRepository):
    def __init__(self):
        super().__init__(400)


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    server = RatingServer()
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])
        server.logger.info(f'repository: found tables: {[x for x in server.db.meta["tables"]]}')

    server.register_method('/api/v1/rating', get_user_rating, 'GET')
    server.register_method('/api/v1/rating', set_user_rating, 'PUT')
    server.register_method('/manage/health', health, 'GET')
    server.run(host, port)
