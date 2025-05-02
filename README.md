# Deadlock Detection and Recovery Using Suspension and Checkpointing

## Overview

This project simulates a multi-process system that can experience deadlocks and recover from them using a safe and efficient strategy. Instead of terminating or rolling back processes, the system suspends one process involved in the deadlock, saves its state (checkpoint), and restores it later when the system is safe.

The simulation uses a Resource Allocation Graph (RAG) to detect deadlocks, releases held resources upon suspension, and ensures that recovery is smooth, data-safe, and efficient.


## Key Features

- Simulates a dynamic environment with multiple processes and resources
- Detects deadlocks using cycle detection in a Resource Allocation Graph
- Suspends the process holding the fewest resources to minimize impact
- Saves process state using checkpointing (held + requested resources)
- Releases held resources to allow other processes to continue
- Immediately reassigns freed resources to waiting processes
- Restores suspended processes when all their required resources are available
- Logs all steps of the simulation
- Visualizes before and after states using Graphviz diagrams
