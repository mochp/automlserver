from celery import Celery
celery = Celery("tasks", broker="amqp://guest:guest@119.29.151.45:5672", backend="amqp")  使用RabbitMQ作为载体, 回调也是使用rabbit作为载体


@celery.task(name="doing")  # 异步任务，需要命一个独一无二的名字
def doing(s, b):
    print("开始任务")
    logging.warning("开始任务--{}".format(s))
    time.sleep(s)
    return s+b
