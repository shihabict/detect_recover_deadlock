# class RecoveryManager:
#     def __init__(self, environment):
#         self.env = environment
#
#     def terminate_least_holding_process(self, deadlocked_processes):
#         """
#         Among the deadlocked processes, find the one holding the fewest resources and terminate it.
#         """
#         if not deadlocked_processes:
#             print("No processes to recover.")
#             return
#
#         # Filter to only process nodes (exclude resources)
#         process_list = [pid for pid in deadlocked_processes if pid in self.env.processes]
#
#         # Find the process holding the fewest resources
#         process_to_kill = min(
#             process_list,
#             key=lambda pid: len(self.env.processes[pid].held_resources)
#         )
#
#         print(f"\n🛑 Terminating process {process_to_kill} to recover from deadlock.")
#
#         # Release all resources held by the process
#         for rid in self.env.processes[process_to_kill].held_resources:
#             self.env.resources[rid].allocated_to = None
#             print(f"Released resource {rid} from {process_to_kill}")
#
#         # Remove the process
#         del self.env.processes[process_to_kill]


# from utils.logger import logger
#
# class RecoveryManager:
#     def __init__(self, environment):
#         self.env = environment
#
#     def suspend_blocking_process(self, deadlocked_processes):
#         if not deadlocked_processes:
#             logger.info("No deadlocked processes to suspend.")
#             return
#
#         # Filter to only valid processes
#         process_list = [pid for pid in deadlocked_processes if pid in self.env.processes]
#
#         # Find the process with fewest resources held
#         min_held = min(len(self.env.processes[pid].held_resources) for pid in process_list)
#         candidates = [pid for pid in process_list if len(self.env.processes[pid].held_resources) == min_held]
#
#         # Tie-breaker: lowest PID
#         process_to_suspend = min(candidates)
#
#         proc = self.env.processes[process_to_suspend]
#         proc.status = "blocked"
#
#         logger.info(f"🛑 Suspended process P{process_to_suspend} to resolve deadlock.")
#         logger.info(f"Process P{process_to_suspend} status: {proc.status}")
#         logger.info(f"Held resources: {proc.held_resources}")
#         logger.info(f"Waiting for: {proc.requested_resources}")
#
from utils.logger import logger
import copy

class RecoveryManager:
    def __init__(self, environment):
        self.env = environment
        self.checkpoints = {}  # PID -> saved process state

    def suspend_with_checkpoint(self, deadlocked_nodes):
        """
        Suspend a process involved in deadlock, save its state, and release its held resources.
        """
        if not deadlocked_nodes:
            logger.info("No deadlocked nodes to suspend.")
            return

        process_ids = []
        for node in deadlocked_nodes:
            if isinstance(node, str) and node.startswith("P"):
                try:
                    pid = int(node[1:])
                    if pid in self.env.processes:
                        process_ids.append(pid)
                except ValueError:
                    logger.warning(f"Invalid process node format: {node}")

        if not process_ids:
            logger.warning("No valid processes found in deadlock cycle. Skipping suspension.")
            return

        # Choose process with fewest held resources
        min_held = min(len(self.env.processes[pid].held_resources) for pid in process_ids)
        candidates = [pid for pid in process_ids if len(self.env.processes[pid].held_resources) == min_held]
        process_to_suspend = min(candidates)  # tie-breaker: lowest PID

        proc = self.env.processes[process_to_suspend]

        # Save checkpoint (deep copy of held/requested resources and status)
        self.checkpoints[process_to_suspend] = {
            "held": copy.deepcopy(proc.held_resources),
            "requested": copy.deepcopy(proc.requested_resources),
            "priority": proc.priority,
        }

        # Release all held resources
        # for rid in proc.held_resources:
        #     self.env.resources[rid].allocated_to = None
        #     logger.info(f"💾 Released resource {rid} from suspended P{process_to_suspend}")
        # Release and reassign held resources
        for rid in proc.held_resources:
            self.env.resources[rid].allocated_to = None
            logger.info(f"💾 Released resource {rid} from suspended P{process_to_suspend}")

            # Check if any active process is waiting for this resource
            for other_pid, other_proc in self.env.processes.items():
                if other_pid == process_to_suspend:
                    continue  # skip the suspended process itself

                if rid in other_proc.requested_resources and other_proc.status == "active":
                    other_proc.requested_resources.remove(rid)
                    other_proc.held_resources.add(rid)
                    self.env.resources[rid].allocated_to = other_pid
                    logger.info(f"🎯 Reassigned {rid} to P{other_pid} (was waiting)")
                    break  # assign to only one process

        proc.held_resources.clear()
        proc.status = "blocked"

        logger.info(f"🛑 Suspended P{process_to_suspend} with checkpoint.")
        logger.info(f"Checkpointed state: {self.checkpoints[process_to_suspend]}")
        logger.info(f"Process P{process_to_suspend} is now blocked and will retry later.")

    def restore_suspended_processes(self):
        """
        Attempt to restore blocked processes from checkpoint if their requested AND previously held resources are available.
        """
        for pid, checkpoint in list(self.checkpoints.items()):
            proc = self.env.processes.get(pid)

            if proc and proc.status == "blocked":
                # Combine requested and held resources for availability check
                all_needed = checkpoint["requested"].union(checkpoint["held"])

                can_restore = any(
                    self.env.resources[rid].allocated_to is None for rid in all_needed
                )

                if can_restore:
                    logger.info(f"♻️ Restoring P{pid} from checkpoint...")

                    # Allocate both requested and held resources
                    for rid in checkpoint["requested"]:
                        if self.env.resources[rid].allocated_to is None:
                            self.env.resources[rid].allocated_to = pid
                            proc.held_resources.add(rid)
                            logger.info(f"🔁 Re-allocated requested {rid} to P{pid}")

                    for rid in checkpoint["held"]:
                        if self.env.resources[rid].allocated_to is None:
                            self.env.resources[rid].allocated_to = pid
                            proc.held_resources.add(rid)
                            logger.info(f"🔁 Re-allocated previously held {rid} to P{pid}")

                    proc.requested_resources.clear()
                    proc.status = "active"
                    proc.priority = checkpoint["priority"]

                    logger.info(f"✅ P{pid} is restored and active.")
                    del self.checkpoints[pid]

                else:
                    logger.info(f"⏳ P{pid} still waiting: some resources unavailable.")

    # def restore_suspended_processes(self):
    #     """
    #     Attempt to restore blocked processes from checkpoint if their requested resources are now available.
    #     """
    #     for pid, checkpoint in list(self.checkpoints.items()):
    #         proc = self.env.processes.get(pid)
    #         # proc['held'] = checkpoint['held']
    #         if proc and proc.status == "blocked":
    #             can_restore = all(
    #                 self.env.resources[rid].allocated_to is None
    #                 for rid in checkpoint["requested"] or checkpoint["held"]
    #             )
    #
    #             if can_restore:
    #                 logger.info(f"♻️ Restoring P{pid} from checkpoint...")
    #
    #                 # Allocate requested resources
    #                 for rid in checkpoint["requested"]:
    #                     self.env.resources[rid].allocated_to = pid
    #                     proc.held_resources.add(rid)
    #                     logger.info(f"🔁 Re-allocated {rid} to P{pid}")
    #
    #                 # Restore state
    #                 proc.requested_resources.clear()
    #                 proc.status = "active"
    #                 proc.priority = checkpoint["priority"]
    #
    #                 logger.info(f"✅ P{pid} is restored and active.")
    #                 del self.checkpoints[pid]
    #             else:
    #                 logger.info(f"⏳ P{pid} still waiting: some resources unavailable.")

