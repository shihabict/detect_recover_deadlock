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
env.request_resource("P0", "R1")  # P0 now waits for R1
env.request_resource("P1", "R0")  # P1 now waits for R0
env.request_resource("P1", "R2")
env.request_resource("P1", "R3")


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

# Graph Visualization
from visualization.visualizer import RAGVisualizer

visualizer = RAGVisualizer(rag)
visualizer.draw(filename='rag_before_output.pdf')  # Will generate rag_output.png
print(0)


# recovery

from recovery.recovery import RecoveryManager

if has_deadlock:
    print("\n⚠️ Deadlock Detected!")
    print("Involved Nodes:", involved)

    # Recover from deadlock
    recovery = RecoveryManager(env)
    recovery.terminate_least_holding_process(involved)

    # Rebuild and re-check graph
    rag = builder.build_rag()
    builder.print_edges()

    detector = DeadlockDetector(rag)
    has_deadlock, involved = detector.detect_deadlock()

    if not has_deadlock:
        print("\n✅ Deadlock successfully resolved.")
    else:
        print("\n❌ Deadlock still persists. More recovery needed.")

    visualizer = RAGVisualizer(rag)
    visualizer.draw(filename='rag_after_recovery.pdf')

