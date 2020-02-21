from kombu import Queue
import re
from datetime import timedelta
from celery.schedules import crontab


BROKER_URL = "amqp://guest@localhost//"  # 使用redis 作为消息代理
CELERY_RESULT_BACKEND = "rpc://guest@localhost//"  # 任务结果存在Redis

CELERY_TASK_DEFAULT_QUEUE = "default"   # 设置默认队列名为 default
CELERY_RESULT_SERIALIZER = "json"  # 可读性更好的JSON
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，


# CELERY_QUEUES = (  # 定义任务队列
#     Queue("default", routing_key="default"),  # 路由键以“task.”开头的消息都进default队列
#     Queue("queues_pdf", routing_key="pdf"),  # 路由键以“task.”开头的消息都进default队列
#     Queue("queues_jpg", routing_key="jpg"),  # 路由键以“A.”开头的消息都进tasks_A队列
# )

# CELERY_ROUTES = (
#    [
#        ("tasks.default", {"queue": "default"}), # 将add任务分配至队列 default
#        ("tasks.pdf", {"queue": "queues_pdf"}),# 将taskA任务分配至队列 tasks_A
#        ("tasks.jpg", {"queue": "queues_jpg"}),# 将taskB任务分配至队列 tasks_B
#    ],
# )


#  
# CELERY_TASK_DEFAULT_EXCHANGE = "tasks"
# CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "topic"
# CELERY_TASK_DEFAULT_ROUTING_KEY = "task.default"