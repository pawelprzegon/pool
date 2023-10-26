from dataclasses import dataclass, field


@dataclass
class TrackThreads:
    thread: dict = field(init=False)

    def __post_init__(self):
        self.thread = {}

    def set_thread(self, track, thread):
        print('set_thread')
        self.thread[track] = thread

    def get_thread(self, track):
        print('get_thread')
        return self.thread[track]