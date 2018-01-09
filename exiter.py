import signal


class Exiter:

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)
        self.should_exit = False

    def exit(self, signum, frame):
        self.should_exit = True
