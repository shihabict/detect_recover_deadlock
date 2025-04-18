# class Process:
#     def __init__(self, pid):
#         self.pid = pid
#         self.held_resources = set()
#         self.requested_resources = set()
#
#     def __repr__(self):
#         return f"Process({self.pid})"

class Process:
    def __init__(self, pid: int, priority: int = 5):
        self.pid = pid
        self.priority = priority
        self.held_resources = set()
        self.requested_resources = set()
        self.status = "active"  # can be 'active' or 'blocked'

    def __repr__(self):
        return f"Process(P{self.pid}, priority={self.priority}, status={self.status})"
