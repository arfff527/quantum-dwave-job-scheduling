# QUBO-based Job Scheduling with D-Wave

This repository provides an implementation of a **job scheduling optimization model** using **QUBO (Quadratic Unconstrained Binary Optimization)**. The model is designed to assign jobs to machines in a factory setting with constraints, and it leverages both CPU-based solvers and D-Wave’s quantum annealers.

---

## 📂 Project Structure

- **`qubo_building.py`**
  - Builds the QUBO matrix for the scheduling problem.
  - Implements constraints:
    1. Each job can only run on one machine.
    2. A job can only run on specific machines.
    3. Adds penalty functions to reduce execution time (`machine_welcome_factor*0.12 + processing_time`).
  - Provides utility functions:
    - `getQuboMatrix()`: construct QUBO matrix.
    - `find_job_processing_time()`: fetch job-machine processing time.
    - `cal_welcome_factor()`: calculate machine popularity (welcome factor).
    - `decoding_result()`: decode solver results into schedules.
    - `validation()`: check feasibility of solutions.
    - `generate_factory_data()`: build problem instances from input data.

- **`main.py`**
  - Main entry script to:
    - Generate problem data.
    - Build the QUBO model.
    - Solve it using either:
      - **CPU solver** (`QBSolv`).
      - **QPU solver** (D-Wave hybrid workflow).
    - Validate the solution.
    - Visualize results as a Gantt chart.

- **`factory_data_encoding.py`**
  - Preprocesses factory input data (orders and UPH).
  - Functions:
    - `cal_uph_one_date()`: compute UPH for a given date.
    - `cal_uph_one_month()`: compute UPH across a month.
    - `order_divide()`: split and reorganize jobs if order quantity exceeds thresholds.
  - Outputs job lists compatible with QUBO encoding.

- **`gantt_visualization.py`**
  - Visualizes scheduling results as Gantt charts.
  - Functions:
    - `draw_gantt()`: plot job-machine allocation.
    - `solution_visualization()`: generate and save Gantt charts with makespan and runtime details.

---Result visualization
3. Result visualization
 
Figure 2 optimized solution vs greedy solution
 
Figure 3optismized solution vs random solution
<img width="487" height="555" alt="image" src="https://github.com/user-attachments/assets/1d111e81-205b-4058-8f4d-be31bb9b137b" />



## ⚙️ Requirements

- Python 3.8+
- Dependencies:
  - `matplotlib`
  - `numpy`
  - `dwave-qbsolv`
  - `dwave-hybrid`
- Data files:
  - `LCFC data/t_ml_assy_atb.csv`
  - `LCFC data/t_ml_line_uph.csv`
  - `data_processing/t_ml_line_uph.csv`

---

## 🚀 Usage

1. **Prepare data**
   - Place the required CSV files in the paths specified in `factory_data_encoding.py`.

2. **Run the solver**
   ```bash
   python main.py

3. **Choose solver**
By default, QBSolv (CPU solver) is used.
Uncomment QPU solver section in main.py to run on D-Wave QPU.

   
