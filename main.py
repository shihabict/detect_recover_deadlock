# from core.environment import Environment
# from core.graph_builder import GraphBuilder
# # Create environment
# env = Environment()
#
# # Add processes
# env.add_process("P0")
# env.add_process("P1")
#
# # Add resources
# env.add_resource("R0")
# env.add_resource("R1")
# env.add_resource("R2")
# env.add_resource("R3")
#
# # Allocate initial resources
# env.request_resource("P0", "R0")
# env.request_resource("P1", "R1")
#
# # Induce deadlock scenario
# env.request_resource("P0", "R1")  # P0 now waits for R1
# env.request_resource("P1", "R0")  # P1 now waits for R0
# env.request_resource("P1", "R2")
# env.request_resource("P1", "R3")
#
#
# # build graph
# builder = GraphBuilder(env)
# rag = builder.build_rag()
# builder.print_edges()
#
# # detect deadlock
#
# from detection.detector import DeadlockDetector
#
# detector = DeadlockDetector(rag)
# has_deadlock, involved = detector.detect_deadlock()
#
# if has_deadlock:
#     print("\n⚠️ Deadlock Detected!")
#     print("Involved Nodes:", involved)
# else:
#     print("\n✅ No Deadlock Detected.")
#
# # Graph Visualization
# from visualization.visualizer import RAGVisualizer
#
# visualizer = RAGVisualizer(rag)
# visualizer.draw(filename='rag_before_output.pdf')  # Will generate rag_output.png
# print(0)
#
#
# # recovery
#
# from recovery.recovery import RecoveryManager
#
# if has_deadlock:
#     print("\n⚠️ Deadlock Detected!")
#     print("Involved Nodes:", involved)
#
#     # Recover from deadlock
#     recovery = RecoveryManager(env)
#     recovery.terminate_least_holding_process(involved)
#
#     # Rebuild and re-check graph
#     rag = builder.build_rag()
#     builder.print_edges()
#
#     detector = DeadlockDetector(rag)
#     has_deadlock, involved = detector.detect_deadlock()
#
#     if not has_deadlock:
#         print("\n✅ Deadlock successfully resolved.")
#     else:
#         print("\n❌ Deadlock still persists. More recovery needed.")
#
#     visualizer = RAGVisualizer(rag)
#     visualizer.draw(filename='rag_after_recovery.pdf')
#

from core.environment import Environment
from core.graph_builder import GraphBuilder
from detection.detector import DeadlockDetector
from recovery.recovery import RecoveryManager
from visualization.visualizer import RAGVisualizer
from utils.logger import logger

# Step 1: Setup environment
env = Environment()

# Add 2 processes and 2 resources
env.add_process(0, priority=2)
env.add_process(1, priority=3)
# env.add_process(2, priority=3)

env.add_resource("R0")
env.add_resource("R1")
env.add_resource("R2")
env.add_resource("R3")
env.add_resource("R4")
# env.add_resource("R5")
# env.add_resource("R6")
# env.add_resource("R7")

# Step 2: Create allocation & wait that causes deadlock
# P0 gets R0, then requests R1
env.request_resource(0, "R0")
env.request_resource(0,"R2")
env.request_resource(0,"R3")
env.request_resource(1, "R1")
# env.request_resource(2, "R4")
# env.request_resource(2, "R5")
# env.request_resource(1, "R6")
# env.request_resource(2, "R7")
# env.request_resource(2, "R6")


# P1 gets R1, then requests R0
env.request_resource(0, "R1")
env.request_resource(1, "R0")

# Step 3: Build graph and detect deadlock
builder = GraphBuilder(env)
rag = builder.build_rag()
builder.print_edges()

detector = DeadlockDetector(rag)
has_deadlock, involved = detector.detect_deadlock()

if has_deadlock:
    logger.info("⚠️ Deadlock Detected!")
    logger.info(f"Involved nodes: {involved}")

    rag = builder.build_rag()
    visualizer = RAGVisualizer(rag)
    visualizer.draw(filename='rag_before_suspension_case3')

    # Step 4: Suspend one of the deadlocked processes
    recovery = RecoveryManager(env)
    # recovery.suspend_blocking_process(involved)
    recovery.suspend_with_checkpoint(involved)


    # Step 5: Visualize RAG after suspension
    rag = builder.build_rag()
    visualizer = RAGVisualizer(rag)
    visualizer.draw(filename='rag_after_suspension_case3')

    # Step 6: Manually release a resource to test retry mechanism
    env.release_resource(0, "R0")
    env.release_resource(0, "R1")
    env.release_resource(0, "R2")
    env.release_resource(0, "R3")
    print(0)
    # Step 8: Attempt to restore suspended processes
    recovery.restore_suspended_processes()

    # Step 9: Visualize final state
    rag = builder.build_rag()
    visualizer.draw(filename='rag_final_restored_case3')
else:
    logger.info("✅ No Deadlock Detected.")
    visualizer = RAGVisualizer(rag)
    visualizer.draw(filename='rag_normal')
