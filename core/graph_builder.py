import networkx as nx

# class GraphBuilder:
#     def __init__(self, environment):
#         self.env = environment
#         self.graph = nx.DiGraph()  # Directed graph
#
#     def build_rag(self):
#         self.graph.clear()
#
#         # Add nodes for processes and resources
#         for pid in self.env.processes:
#             self.graph.add_node(pid, type='process')
#
#         for rid in self.env.resources:
#             self.graph.add_node(rid, type='resource')
#
#         # Add allocation edges: resource -> process
#         for rid, res in self.env.resources.items():
#             if res.allocated_to is not None:
#                 self.graph.add_edge(rid, res.allocated_to)
#
#         # Add request edges: process -> resource
#         for pid, proc in self.env.processes.items():
#             for rid in proc.requested_resources:
#                 self.graph.add_edge(pid, rid)
#
#         return self.graph
#
#     def print_edges(self):
#         print("RAG edges:")
#         for u, v in self.graph.edges:
#             print(f"{u} → {v}")



# class GraphBuilder:
#     def __init__(self, environment):
#         self.env = environment
#         self.graph = nx.DiGraph()
#
#     def build_rag(self):
#         self.graph.clear()
#
#         # Add process nodes (e.g., P0, P1)
#         for pid in self.env.processes:
#             self.graph.add_node(f"P{pid}", type='process')
#
#         # Add resource nodes
#         for rid in self.env.resources:
#             self.graph.add_node(str(rid), type='resource')  # Ensure resource ID is str
#
#         # Add allocation edges: resource → process
#         for rid, res in self.env.resources.items():
#             if res.allocated_to is not None:
#                 self.graph.add_edge(str(rid), f"P{res.allocated_to}")
#
#         # Add request edges: process → resource
#         for pid, proc in self.env.processes.items():
#             for rid in proc.requested_resources:
#                 self.graph.add_edge(f"P{pid}", str(rid))
#
#         return self.graph
#
#     def print_edges(self):
#         print("RAG edges:")
#         for u, v in self.graph.edges:
#             print(f"{u} → {v}")
#

class GraphBuilder:
    def __init__(self, environment):
        self.env = environment
        self.graph = nx.DiGraph()

    def build_rag(self):
        self.graph.clear()

        # Add process nodes (e.g., P0, P1)
        for pid, proc in self.env.processes.items():
            self.graph.add_node(f"P{pid}", type='process')

        # Add resource nodes (e.g., R0, R1)
        for rid in self.env.resources:
            self.graph.add_node(str(rid), type='resource')

        # Add allocation edges: resource → process
        for rid, res in self.env.resources.items():
            if res.allocated_to is not None:
                self.graph.add_edge(str(rid), f"P{res.allocated_to}")

        # Add request edges: process → resource (only if process is active)
        for pid, proc in self.env.processes.items():
            if proc.status == "active":
                for rid in proc.requested_resources:
                    self.graph.add_edge(f"P{pid}", str(rid))

        return self.graph

    def print_edges(self):
        print("RAG edges:")
        for u, v in self.graph.edges:
            print(f"{u} → {v}")
