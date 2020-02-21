1、项目放到 /opt 目录下

2、指令

#清除队列
rabbitmqctl list_queues
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app

#简单启动
celery -A tasks worker -l info
#多线程后台启动
celery multi start w1 -A proj -l info --pidfile=./logs/run/%n.pid --logfile=./logs/log/%n%I.log
#暴力关闭
celery multi stop w1 -A proj -l info
#等待任务结束关闭
celery multi stopwait w1 -A proj -l info