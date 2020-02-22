from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('automl', broker="amqp://apabi:10NsS2mM@47.94.226.184:5672//",
             backend="rpc://apabi:10NsS2mM@47.94.226.184:5672//")

# Optional configuration, see the application user guide
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Shanghai',
    # enable_utc=True,
    result_expires=3600
)

if __name__ == '__main__':
    app.start()
