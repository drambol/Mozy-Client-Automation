#!/usr/bin/env python
# -*- coding:utf-8 -*-

from kombu import Queue, Exchange

from configuration.global_config_loader import GLOBAL_CONFIG

###############################################
## config file for Celery Daemon             ##
###############################################

# default Redis/RabbitMQ broker
BROKER_URL = 'redis://{url}:{port}/0'.format(url=GLOBAL_CONFIG.get('REDIS').get('URL'), port=GLOBAL_CONFIG.get('REDIS').get('PORT'))

# default Redis/RabbitMQ backend
CELERY_RESULT_BACKEND = 'redis://{url}:{port}/0'.format(url=GLOBAL_CONFIG.get('REDIS').get('URL'), port=GLOBAL_CONFIG.get('REDIS').get('PORT'))


ENABLE_UTC = True

#########################################################################
# prefork = 4 by default, the first worker may fetch too many tasks, so #
# pick only 1 task, then follow robin-round policy with enough workers. #
#########################################################################
CELERYD_CONCURRENCY = 1
CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']


CELERY_QUEUES = (
     Queue('default', Exchange('default'), routing_key='default'),
)

CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'


def route_task(name, args, kwargs, options, task=None, **kw):

    if name == 'task_dispatch.tasks.worker_setup':
        return {
            'queue': 'default',
            'exchange': 'default',
            'routing_key': 'default',
        }


CELERY_ROUTES = (route_task, )

