import time
from threading import Timer

class QuizTimer:
    def __init__(self, timeout, time_up_callback):
        self.timeout = timeout
        self.time_up_callback = time_up_callback
        self.timer = None
        self.remaining_time = timeout

    def start(self):
        self.timer = Timer(self.timeout, self.time_up_callback)
        self.timer.start()

    def restart(self):
        if self.timer:
            self.timer.cancel()
        self.remaining_time = self.timeout
        self.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
            self.remaining_time = self.timeout