#!/usr/bin/env python
# -*- coding:utf-8 -*-


from celery import Celery
app = Celery('task_dispatch', include=['task_dispatch.tasks'])
app.config_from_object('task_dispatch.celeryconfig')


if __name__ == '__main__':
    app.start()