#!/usr/bin/env python
#
# Copyright (c) Maginatics, Inc. All rights reserved.
# For more information, please see the COPYRIGHT file in the top-level
# directory.
#
# Stewards: Christine Gong
import re

from lib.singleton import Singleton
from lib.cmdhelper import CmdHelper
from task_dispatch import tasks
from configuration.global_config_loader import GLOBAL_CONFIG
from lib.elasticsearchhelper import ElasticsearchHelper


class CeleryHelper(object):
    """
    wrapeer that encapsulate Celery functionality
    """

    __metaclass__ = Singleton
    celery_app = 'task_dispatch.tasks'



    @classmethod
    def check_status(cls):
        cmd = "status"
        output = cls.__run_celery_command(cmd)
        return output

    @classmethod
    def inspect_active_queues(cls):
        cmd = "inspect active_queues"
        output = cls.__run_celery_command(cmd)
        machine = []
        worker_name = ""
        for line in output.splitlines():
            print line
            print "------------------"
            re_test = re.match(r'->\s+.*@(.*):\s+OK',line)
            if re_test:
                worker_name = re_test.group(1)
                # machine.append(worker_name)
            re_status = re.match(r'\s+\*\s+(.*)', line)
            if re_status:
                import ast
                print ast.literal_eval(re_status.group(1))["exchange"]["passive"]
                if not ast.literal_eval(re_status.group(1))["exchange"]["passive"]:
                    machine.append(worker_name)


        return machine

    @classmethod
    def __run_celery_command(cls, command):
        cmd = "celery -A {app} {cmd}".format(app=cls.celery_app, cmd=command)
        output = CmdHelper.run(cmd)
        return output


    @classmethod
    def add_worker(cls,  worker_name, queue_name, ):
        # celery control add_consumer queue exchange direct rkey
        #        $ celery control -d w1.e.com add_consumer queue_name
        cmd = 'celery control -A {app} -d {worker_name} add_consumer {queue_name}'.format(app=cls.celery_app, worker_name=worker_name, queue_name=queue_name)
        output = CmdHelper.run(cmd)
        return output

    @classmethod
    def delete_worker(cls,  worker_name, queue_name):
        # celery control add_consumer queue exchange direct rkey
        #        $ celery control -d w1.e.com add_consumer queue_name
        cmd = 'celery control -A {app} -d {worker_name} cancel_consumer {queue_name}'.format(app=cls.celery_app, worker_name=worker_name, queue_name=queue_name)
        output = CmdHelper.run(cmd)
        return output

    @classmethod
    def detach_from_queue(cls,queue_name):
        cmd = 'celery control -A {app}  cancel_consumer {queue_name}'.format(app=cls.celery_app, queue_name=queue_name)
        output = CmdHelper.run(cmd)
        return output

    @classmethod
    def run_task(cls, task, args=None, queue=None, task_id=None, worker_name=None):
        """

        :param task:
        :param args:
        :param queue:
        :return:
        """
        task_handle = getattr(tasks, task)
        if task_handle:
            if queue:
                result = task_handle.apply_async(args=[args], queue=queue, task_id=task_id, worker_name=worker_name)
            else:
                result = task_handle.apply_async(args=[args],task_id=task_id, worker_name=worker_name)
            return result
        else:
            raise RuntimeError("tasks not defined %s" % task)

    @classmethod
    def inspect_active_workers(cls):
        cmd = "inspect active"
        output = cls.__run_celery_command(cmd)
        machine = []
        # worker_name = ""
        for line in output.splitlines():

            re_test = re.match(r'->\s+(.*):\s+OK',line)
            if re_test:
                worker_name = re_test.group(1)
                CeleryHelper.delete_worker(worker_name=worker_name, queue_name="worker_setup")
                machine.append(worker_name)

        return machine

    @classmethod
    def get_online_workers(cls):
        """
        :return:
        """
        online_workers  = []
        cmd = 'celery -A {app} control heartbeat'.format(app=cls.celery_app)
        output = CmdHelper.run(cmd)
        for line in output.splitlines():
            re_test = re.match(r'->\s+(.*):\s+OK',line)
            if re_test:
                worker_name = re_test.group(1)
                online_workers.append(worker_name)
        return online_workers


    @classmethod
    def update_task_status(cls, task, testrun_id, result=None):
        task_status = result or tasks.run_automation.AsyncResult(task).status
        task_id = task
        task_body = {
            'id': task,
            'testrun_id': testrun_id,
            'status': task_status
        }

        url = GLOBAL_CONFIG['ELASTICSEARCH'].get('URL') or "http://localhost"
        port = GLOBAL_CONFIG['ELASTICSEARCH'].get('PORT') or "8080"
        es = ElasticsearchHelper(url, port)
        result = es.index(index='task', doc_type='task', body=task_body, _id=task_id)
        return result


if __name__ == '__main__':
    print CeleryHelper.inspect_active_workers()
