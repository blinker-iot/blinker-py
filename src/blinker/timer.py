# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import math
import sched
import uuid


class Timing(object):
    """定时 """

    def __init__(self):
        self.id = uuid.uuid1().hex
        self.task = ""
        self.task_data = ""

    async def set(self, task, data):
        self.task = task
        self.task_data = data

    async def get(self):
        pass

    async def delete(self):
        pass


class TimingTasks(object):
    """定时任务 """

    tasks = {}

    def add(self, task):
        if task["ena"] == 0:
            self.disable(task["task"])
        else:
            hour = math.floor(task["tim"] / 60)
            minute = task["tim"] % 60
            day_of_week = []
            for i in range(len(task["day"])):
                if task[i] == "1":
                    day_of_week.append(i)
            conf = {"minute": minute, "hour": hour}
            if len(day_of_week) == 1:
                conf["dayOfWeek"] = day_of_week[0]
            elif len(day_of_week) > 1:
                conf["dayOfWeek"] = day_of_week

            self.tasks[task["task"]] = sched.scheduler()

    def delete(self, task_id: str):
        pass

    def disable(self, task_id: str):
        pass

    def enable(self, task_id: str):
        pass

    def load(self, tasks):
        for task in tasks:
            if task.ena == 1:
                self.add(task)


class CountDownTimer(object):
    """倒计时功能 """

    def __init__(self):
        self.countdown_timer = None
        self.countdown_timer2 = None

    async def set(self, data):
        pass

    async def get(self):
        pass

    async def clear(self):
        pass
