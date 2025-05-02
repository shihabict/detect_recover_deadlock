# Deadlock Detection and Recovery Using Suspension and Checkpointing

## Overview

This project simulates a multi-process system that can experience deadlocks and recover from them using a safe and efficient strategy. Instead of terminating or rolling back processes, the system suspends one process involved in the deadlock, saves its state (checkpoint), and restores it later when the system is safe.

The simulation uses a Resource Allocation Graph (RAG) to detect deadlocks, release held resources upon suspension, and ensure smooth, data-safe, and efficient recovery.


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

## System Architecture

The system is structured around modular components that simulate how deadlocks are handled in operating systems. Below is a high-level view of how the components interact:

## How It Works

### 1. Deadlock Detection
The system builds a Resource Allocation Graph (RAG) where:
- Nodes = Processes and Resources
- Edges = Request or Allocation relations
A cycle in this graph indicates a deadlock. The system uses NetworkX to detect this cycle.

### 2. Process Suspension and Checkpointing
When a deadlock is detected:
- The system selects one process to suspend (based on the fewest held resources)
- The process's state is checkpointed (held + requested resources)
- All held resources are released

### 3. Resource Reassignment
Once a resource is released:
- The system immediately checks if any other process is waiting for it
- If so, the resource is reassigned automatically without delay

### 4. Process Restoration
Suspended processes are monitored:
- When all the resources they previously held and requested become available, they are restored from the checkpoint and resume execution
