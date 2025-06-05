# 🚗 Traveling Salesman Problem Solver

A Python implementation solving the classic TSP using multiple algorithmic approaches:
- **Greedy Algorithm**
- **Backtracking**
- **Dynamic Programming** (Held-Karp)

## 📌 Problem Definition
Given a list of cities and distances between them, find the **shortest possible route** that:
- Visits each city exactly once
- Returns to the origin city

```python
# Example Input
cities = ["A", "B", "C"]
distance_matrix = [
    [0, 10, 15],  # A to A, B, C
    [10, 0, 20],   # B to A, B, C
    [15, 20, 0]    # C to A, B, C
]

```
## 🧠 Algorithms Implemented

| Method         | Time Complexity | Best For                     |
|----------------|-----------------|------------------------------|
| **Greedy**     | O(n²)           | Quick approximate solutions  |
| **Backtracking** | O(n!)          | Small datasets (n ≤ 10)      |
| **DP (Held-Karp)** | O(n²2ⁿ)      | Medium datasets (n ≤ 20)     |

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Visualization**: Matplotlib
- **Data Structures**:
  - Adjacency matrix
  - Priority queues
- **Optimizations**:
  - Memoization
  - Pruning
