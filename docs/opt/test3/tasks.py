import os
import time
from datetime import datetime

from celery import Celery


app = Celery("tasks", broker="amqp://guest@localhost//",
                backend="rpc://guest@localhost//")


@app.task(name='task.query_users')
def query_mysql(flag):
    time.sleep(5)
    return "hello~" + str(flag)

if __name__ == "__main__":
    app.start()