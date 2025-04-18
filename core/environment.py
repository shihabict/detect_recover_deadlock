# from .process import Process
# from .resource import Resource
#
# class Environment:
#     def __init__(self):
#         self.processes = {}
#         self.resources = {}
#
#     def add_process(self, pid):
#         if pid not in self.processes:
#             self.processes[pid] = Process(pid)
#
#     def add_resource(self, rid):
#         if rid not in self.resources:
#             self.resources[rid] = Resource(rid)
#
#     def request_resource(self, pid, rid):
#         process = self.processes[pid]
#         resource = self.resources[rid]
#
#         if resource.allocated_to is None:
#             resource.allocated_to = pid
#             process.held_resources.add(rid)
#             print(f"{pid} allocated {rid}")
#         else:
#             process.requested_resources.add(rid)
#             print(f"{pid} is waiting for {rid}")
#
#     def release_resource(self, pid, rid):
#         process = self.processes[pid]
#         resource = self.resources[rid]
#
#         if rid in process.held_resources:
#             resource.allocated_to = None
#             process.held_resources.remove(rid)
#             print(f"{pid} released {rid}")

from .process import Process
from .resource import Resource
from utils.logger import logger

class Environment:
    def __init__(self):
        self.processes = {}
        self.resources = {}

    def add_process(self, pid, priority=5):
        if pid not in self.processes:
            self.processes[pid] = Process(pid, priority)
            logger.info(f"Created process P{pid} with priority {priority}")

    def add_resource(self, rid):
        if rid not in self.resources:
            self.resources[rid] = Resource(rid)
            logger.info(f"Added resource {rid}")

    def request_resource(self, pid, rid):
        process = self.processes[pid]
        resource = self.resources[rid]

        if process.status == "blocked":
            logger.info(f"⏸️ Process P{pid} is blocked. Request for {rid} is deferred.")
            return

        if resource.allocated_to is None:
            resource.allocated_to = pid
            process.held_resources.add(rid)
            logger.info(f"✅ P{pid} allocated {rid}")
            self.retry_blocked_processes()
        else:
            resource.requested_from = pid
            process.requested_resources.add(rid)
            logger.info(f"❌ P{pid} is waiting for {rid} (held by P{resource.allocated_to})")

    # def release_resource(self, pid, rid):
    #     process = self.processes[pid]
    #     resource = self.resources[rid]
    #
    #     if rid in self.processes[pid].held_resources:
    #         self.resources[rid].allocated_to = None
    #         self.processes[pid].held_resources.remove(rid)
    #         logger.info(f"🔓 P{pid} released {rid}")
    #         self.retry_blocked_processes()

    def release_resource(self, pid, rid):
        process = self.processes[pid]
        resource = self.resources[rid]

        if rid in process.held_resources:
            process.held_resources.remove(rid)
            resource.allocated_to = None
            logger.info(f"🔓 P{pid} released {rid}")

            # Now check if any other process is requesting this resource
            for other_pid, other_proc in self.processes.items():
                if rid in other_proc.requested_resources and other_proc.status == "active":
                    # Assign it immediately to the first requester
                    other_proc.requested_resources.remove(rid)
                    other_proc.held_resources.add(rid)
                    resource.allocated_to = other_pid

                    logger.info(f"🎯 {rid} immediately reassigned to P{other_pid} (was waiting)")
                    break


    def retry_blocked_processes(self):
        logger.info("🔄 Retrying blocked processes...")

        for pid, process in self.processes.items():
            if process.status == "blocked":
                still_waiting = False

                for rid in process.requested_resources.copy():
                    resource = self.resources[rid]
                    if resource.allocated_to is None:
                        resource.allocated_to = pid
                        process.held_resources.add(rid)
                        process.requested_resources.remove(rid)
                        logger.info(f"🔁 Allocated {rid} to previously blocked P{pid}")
                    else:
                        still_waiting = True

                if not still_waiting and not process.requested_resources:
                    process.status = "active"
                    logger.info(f"✅ Process P{pid} is now unblocked and active again.")
