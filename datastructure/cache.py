from datetime import datetime


class Cache(object):
    def __init__(self, num=500, seconds=60):
        if num == 0:
            self.num = 1
        else:
            self.num = num
        self.time_lastproc = datetime.now()
        self.seconds = seconds
        self.datas = []
        self.result = []
        self.proc = False

    def push(self, data):
        time = datetime.now()
        seconds = (time - self.time_lastproc).seconds
        num = len(self.datas)
        if isinstance(data, dict):
            self.datas.append(data)
            if (num+1) == self.num or seconds > self.seconds:
                self.result.append(tuple(self.datas))
                self.datas.clear()
                self.time_lastproc = time
            self.proc = True

    def pop(self):
        time = datetime.now()
        seconds = (time - self.time_lastproc).seconds
        if len(self.result) > 0:
            return self.result.pop(0)
        elif len(self.result) == 0 and len(self.datas) > 0 and seconds > self.seconds:
            self.result.append(tuple(self.datas))
            self.datas.clear()
            self.time_lastproc = time
            self.proc = False
            return self.result.pop(0)

    def clear(self):
        self.time_lastproc = datetime.now()
        self.datas = []
        self.result = []
        self.proc = False




