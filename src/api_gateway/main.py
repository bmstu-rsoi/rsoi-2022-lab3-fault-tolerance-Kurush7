import copy
import time
from datetime import datetime, timedelta

from flask import request, jsonify, Response

from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer
from qr_server.request_sending import *
from qr_server.RoleManager import role_manager

from gateway.dtos import *
from gateway.utils import *
from gateway.proxy_api import *
from gateway.compound_api import *
from gateway.circuit_breaker import circuitBreaker
from common.job_queue import TASK_QUEUE, run_task_queue
from common.common_api import health


class GatewayServer(FlaskServer):
    def __init__(self):
        super().__init__(400)

    def __method(self, f, *args, **kwargs):  # note: valuable changes; add to original FlaskServer
        ctx = super().create_context(request, self, meta=self.meta)
        ctx.set_managers(self.managers)
        in_msg = '[' + request.method + '] ' + request.url + '/' + request.query_string.decode()
        try:
            start = time.time()
            result = f(ctx, *args, **kwargs)
            end = time.time()
            msecs = int((end - start) * 1000)
            super().info('[' + str(msecs) + ' msecs]' + in_msg)
            if result.raw_data:
                return result.result
            if result.status_code == 200:
                return jsonify(result.result)

            resp = Response(result.result, result.status_code)

            if result.headers is not None:
                for header, value in result.headers.items():
                    resp.headers[header] = value
            return resp

        except Exception as e:
            super().info(in_msg)
            super().exception(e)
            return self.default_err_msg, self.default_err_code


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    meta = {
        'services': {
            'library': QRAddress(f'http://' + config['library_service']['host'], config['library_service']['port']),
            'rating': QRAddress(f'http://' + config['rating_service']['host'], config['rating_service']['port']),
            'reservation': QRAddress(f'http://' + config['reservation_service']['host'],
                                     config['reservation_service']['port']),
        },
    }

    circuitBreaker.register_config(config)
    circuitBreaker.register_meta(meta)

    server = GatewayServer()
    server.set_meta(meta)
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])
        TASK_QUEUE.set_logger(server.logger)
        circuitBreaker.register_logger(server.logger)
        meta['logger'] = server.logger
    run_task_queue()

    server.register_method('/api/v1/libraries', list_libraries_in_city, 'GET')
    server.register_method('/api/v1/libraries/<library_uid>/books', list_books_in_library, 'GET')
    server.register_method('/api/v1/rating', get_user_rating, 'GET')
    server.register_method('/api/v1/reservations', get_user_reservations, 'GET')
    server.register_method('/api/v1/reservations', rent_book, 'POST')
    server.register_method('/api/v1/reservations/<reservation_uid>/return', return_book, 'POST')
    server.register_method('/manage/health', health, 'GET')
    server.run(host, port)
