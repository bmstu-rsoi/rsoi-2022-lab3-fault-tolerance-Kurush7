from typing import List
from qr_server import IQRConfig, MethodResult, QRContext

from .utils import Service, knock_service
from common.job_queue import TASK_QUEUE


class ServiceUnavailableException(Exception):
    def __init__(self, service: Service):
        super().__init__(f"service unavailable: {service}")
        self.service = service


class CircuitBreaker:
    def __init__(self):
        self.config = None
        self.service_fails = {k: 0 for k in Service}
        self.unavailable = {k: False for k in Service}
        self.logger = None

    def register_config(self, config: IQRConfig):
        self.config = config
        self.failure_threshold = config.circuit_breaker.failure_threshold
        self.knock_timeout = config.circuit_breaker.knock_timeout

    def register_meta(self, meta: dict):
        services = meta['services']
        self.service_urls = {
            Service.LIBRARY: services['library'],
            Service.RATING: services['rating'],
            Service.RESERVATION: services['reservation'],
        }

    def register_logger(self, logger):
        self.logger = logger

    def circuit(self, check_services: List[Service] = None, default_response: MethodResult = MethodResult(status_code=400)):
        # check_services - if at least one is unavailable, return instant failure
        def decorator(f):
            def wrapper(ctx: QRContext, *args, **kwargs):
                try:
                    if check_services:
                        failed = sum(self.unavailable[s] for s in check_services)
                        if failed > 0:
                            return default_response

                    res = f(ctx, *args, **kwargs)

                    if check_services:
                        for s in check_services:
                            self.service_fails[s] = 0
                            self.unavailable[s] = False
                    return res
                except ServiceUnavailableException as e:
                    service = e.service
                    self.service_fails[service] += 1
                    if self.service_fails[service] >= self.failure_threshold:
                        self.unavailable[service] = True

                        def callback(ok):
                            self.unavailable[service] = False
                            if self.logger:
                                self.logger.info(f'service revived: {service}')
                        TASK_QUEUE.enqueue(
                            task=lambda: knock_service(self.service_urls[service], throw_exception=True),
                            callback=callback,
                            retry=self.knock_timeout,
                            name='knocking service'
                        )

                    return default_response

            wrapper.__name__ = f.__name__
            return wrapper
        return decorator


circuitBreaker = CircuitBreaker()
