class Lifetime:
    def __init__(self, func):
        self.func = func
        self.task = None

    def start(self, tg):
        assert self.task is None
        self.task = tg.create_task(self.func())
        
    def stop(self):
        assert self.task is not None
        self.task.cancel()
        self.task = None
        
