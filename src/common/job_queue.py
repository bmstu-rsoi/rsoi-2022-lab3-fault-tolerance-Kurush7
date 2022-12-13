import asyncio
import random
import threading
import time

from qr_server import IQRLogger


class TaskQueue:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TaskQueue, cls).__new__(cls)
        return cls.instance

    def set_logger(self, logger: IQRLogger):
        self.logger = logger

    def set_event_loop(self, loop):
        self.loop = loop
        if self.logger:
            self.logger.info('running async task queue')

    def enqueue(self, task, callback=None, retry: int = None, name=None):
        # retry - considers work failed if it threw any exception
        if name is None:
            name = str(task)

        def wrapper():
            try:
                result = task()
                if callback:
                    try:
                        callback(result)
                    except Exception as e:
                        if self.logger:
                            self.logger.error(f'scheduling task {name} executed, but callback failed: {e}')

            except Exception as e:
                if retry is None:
                    if self.logger:
                        self.logger.error(f'scheduled task "{name}" raised: {e}, no retry specified')
                    return
                else:
                    self.logger.warning(f'scheduled task "{name}" failed: retrying in {retry}')
                    #self.loop.call_later_threadsafe(wrapper, retry)
                    self.loop.call_soon_threadsafe(self.loop.call_later, retry, wrapper)

        self.loop.call_soon_threadsafe(wrapper)
        if self.logger:
            self.logger.info(f'scheduling task {name}')

TASK_QUEUE = TaskQueue()

def run_task_queue(queue=TASK_QUEUE):
    def run_queue(q, loop):
        q.set_event_loop(loop)
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_queue, args=(queue, loop))
    t.start()


if __name__ == '__main__':
    run_task_queue()

    def f():
        print('executing')
        time.sleep(5)
        return 3

    def call(res):
        print('res = ', res)

    for i in range(5):
        TASK_QUEUE.enqueue(f, call)
        print(i)