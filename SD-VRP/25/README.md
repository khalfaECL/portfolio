# SD-VRP Project: Split Delivery Vehicle Routing Problem

## 📌 Project Overview
This project addresses the **Split Delivery Vehicle Routing Problem (SD-VRP)**, an advanced variant of the classic Capacitated Vehicle Routing Problem (CVRP). Unlike CVRP, SD-VRP allows multiple vehicles to serve a single customer, optimizing logistics for scenarios where demand exceeds vehicle capacity.

![SD-VRP Visualization](https://via.placeholder.com/400x200?text=SD-VRP+Routes+Example)

## 🎯 Objectives
- Minimize total transportation costs while respecting vehicle capacity constraints
- Fully satisfy customer demands through split deliveries when necessary
- Compare exact and heuristic approaches for different problem scales

## 🛠️ Methodology

### 🔍 Exact Approach
- **Modeling**: MILP formulation using PuLP
- **Solver**: CBC (Coin-or Branch and Cut)
- **Strengths**: Guaranteed optimal solutions for small instances
- **Limitations**: Computational complexity for large problems

### 🧠 Metaheuristic Approach (VNS)
- **Algorithm**: Variable Neighborhood Search
- **Phases**:
  1. Initial solution generation
  2. Local search with neighborhood structures
  3. Shaking for diversification
- **Advantages**: Scalable for large instances


## 💻 Installation & Usage
1. **Requirements**:
   ```bash
   pip install pulp numpy openpyxl

# Process all instances
python main.py

# Process specific case
python main.py --case Case0.txt   