import queue


class Logger:
    def __init__(self):
        self.log_queue = queue.Queue()

    def log(self, msg):
        self.log_queue.put(f"{msg}\n")

    def get_queue(self):
        return self.log_queue

    def close(self):
        self.log_queue.put(None)
