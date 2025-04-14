import networkx as nx

class DeadlockDetector:
    def __init__(self, graph):
        self.graph = graph

    def detect_deadlock(self):
        try:
            # Find cycle (if any)
            cycle = nx.find_cycle(self.graph, orientation="original")
            deadlocked_nodes = [node for edge in cycle for node in edge[:2]]
            deadlocked_nodes = list(set(deadlocked_nodes))  # Unique nodes
            return True, deadlocked_nodes
        except nx.NetworkXNoCycle:
            return False, []
        # except Exception as e:
        #     print(e)