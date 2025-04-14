from graphviz import Digraph

class RAGVisualizer:
    def __init__(self, graph):
        self.graph = graph

    def draw(self, filename='rag', view=True):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')  # Left-to-right layout

        # Add nodes with types
        for node, attr in self.graph.nodes(data=True):
            if attr.get('type') == 'process':
                dot.node(node, shape='ellipse', color='lightblue', style='filled')
            else:
                dot.node(node, shape='box', color='lightgreen', style='filled')

        # Add edges
        for u, v in self.graph.edges:
            dot.edge(u, v)

        # Save and view
        dot.render(filename, view=view)
