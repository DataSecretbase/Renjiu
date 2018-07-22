#coding=utf8
__author__ = 'guozhiwei'
import os

RABBITMQ_CONNECT_INFO = {
    'host':  'localhost',
    'port':  5672,
    'vhost':  '/',
    'username':  'guest',
    'password':  'guest',
    'spec': os.path.dirname(os.path.realpath(__file__))+'/amqp0-9-1.stripped.xml',
}


MAIN_TCP_SERVER_QUEUE_NAME = 'TCP_SERVER_Q'

MAIN_TCP_SERVER_EXCHANGE_NAME = 'MAIN_TCP_SERVER_EXCHANGE_NAME'

WORKER_QUEUE_NAME = 'WORKER_QUEUE_NAME'

EXCHANGE_NAME_WORKER = 'EXCHANGE_NAME_WORKER'

