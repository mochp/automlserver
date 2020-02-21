from celery import Celery
import time

app = Celery('tasks', broker='amqp://guest@localhost//',
             backend="rpc://guest@localhost//")


@app.task
def add(x, y):
    time.sleep(5)
    return x + y

if __name__ == "__main__":
    app.start()