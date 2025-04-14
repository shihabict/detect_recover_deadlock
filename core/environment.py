from .process import Process
from .resource import Resource

class Environment:
    def __init__(self):
        self.processes = {}
        self.resources = {}

    def add_process(self, pid):
        if pid not in self.processes:
            self.processes[pid] = Process(pid)

    def add_resource(self, rid):
        if rid not in self.resources:
            self.resources[rid] = Resource(rid)

    def request_resource(self, pid, rid):
        process = self.processes[pid]
        resource = self.resources[rid]

        if resource.allocated_to is None:
            resource.allocated_to = pid
            process.held_resources.add(rid)
            print(f"{pid} allocated {rid}")
        else:
            process.requested_resources.add(rid)
            print(f"{pid} is waiting for {rid}")

    def release_resource(self, pid, rid):
        process = self.processes[pid]
        resource = self.resources[rid]

        if rid in process.held_resources:
            resource.allocated_to = None
            process.held_resources.remove(rid)
            print(f"{pid} released {rid}")
