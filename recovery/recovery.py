class RecoveryManager:
    def __init__(self, environment):
        self.env = environment

    def terminate_least_holding_process(self, deadlocked_processes):
        """
        Among the deadlocked processes, find the one holding the fewest resources and terminate it.
        """
        if not deadlocked_processes:
            print("No processes to recover.")
            return

        # Filter to only process nodes (exclude resources)
        process_list = [pid for pid in deadlocked_processes if pid in self.env.processes]

        # Find the process holding the fewest resources
        process_to_kill = min(
            process_list,
            key=lambda pid: len(self.env.processes[pid].held_resources)
        )

        print(f"\n🛑 Terminating process {process_to_kill} to recover from deadlock.")

        # Release all resources held by the process
        for rid in self.env.processes[process_to_kill].held_resources:
            self.env.resources[rid].allocated_to = None
            print(f"Released resource {rid} from {process_to_kill}")

        # Remove the process
        del self.env.processes[process_to_kill]
