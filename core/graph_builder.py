import networkx as nx

class GraphBuilder:
    def __init__(self, environment):
        self.env = environment
        self.graph = nx.DiGraph()  # Directed graph

    def build_rag(self):
        self.graph.clear()

        # Add nodes for processes and resources
        for pid in self.env.processes:
            self.graph.add_node(pid, type='process')

        for rid in self.env.resources:
            self.graph.add_node(rid, type='resource')

        # Add allocation edges: resource -> process
        for rid, res in self.env.resources.items():
            if res.allocated_to is not None:
                self.graph.add_edge(rid, res.allocated_to)

        # Add request edges: process -> resource
        for pid, proc in self.env.processes.items():
            for rid in proc.requested_resources:
                self.graph.add_edge(pid, rid)

        return self.graph

    def print_edges(self):
        print("RAG edges:")
        for u, v in self.graph.edges:
            print(f"{u} → {v}")
