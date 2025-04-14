from core.environment import Environment

# Create environment
env = Environment()

# Add processes
env.add_process("P0")
env.add_process("P1")

# Add resources
env.add_resource("R0")
env.add_resource("R1")

# Allocate initial resources
env.request_resource("P0", "R0")
env.request_resource("P1", "R1")

# Induce deadlock scenario
env.request_resource("P0", "R1")  # P0 now waits for R1
env.request_resource("P1", "R0")  # P1 now waits for R0
