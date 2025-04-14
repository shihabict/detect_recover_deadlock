class Process:
    def __init__(self, pid):
        self.pid = pid
        self.held_resources = set()
        self.requested_resources = set()

    def __repr__(self):
        return f"Process({self.pid})"
