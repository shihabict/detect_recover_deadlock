from core.environment import Environment
from core.graph_builder import GraphBuilder
# Create environment
env = Environment()

# Add processes
env.add_process("P0")
env.add_process("P1")

# Add resources
env.add_resource("R0")
env.add_resource("R1")
env.add_resource("R2")
env.add_resource("R3")

# Allocate initial resources
env.request_resource("P0", "R0")
env.request_resource("P1", "R1")

# Induce deadlock scenario
# env.request_resource("P0", "R2")  # P0 now waits for R1
# env.request_resource("P1", "R3")  # P1 now waits for R0
env.request_resource("P0", "R2")
env.request_resource("P1", "R0")


# build graph
builder = GraphBuilder(env)
rag = builder.build_rag()
builder.print_edges()

# detect deadlock

from detection.detector import DeadlockDetector

detector = DeadlockDetector(rag)
has_deadlock, involved = detector.detect_deadlock()

if has_deadlock:
    print("\n⚠️ Deadlock Detected!")
    print("Involved Nodes:", involved)
else:
    print("\n✅ No Deadlock Detected.")

