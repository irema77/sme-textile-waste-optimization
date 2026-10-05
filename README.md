# Optimization-Based Decision Support Tool for Waste Flows in Textile SMEs

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green)
![Optimization](https://img.shields.io/badge/Operations_Research-Linear_Programming-orange)
![TÜBİTAK](https://img.shields.io/badge/Grant-TÜBİTAK_2209--A-red)

## Project Overview
This repository contains the core computational model and decision support framework developed under the **TÜBİTAK 2209-A Research Grant**. The project introduces an optimization-based Decision Support System (DSS) tailored for Small and Medium-sized Enterprises (SMEs) in the textile sector. 

The primary objective is to minimize total waste management costs (recycling and disposal) while adhering to facility capacities, production quotas, and environmental sustainability targets.

## Methodology
The core engine utilizes **Linear Programming (LP)** to model the waste flow network. 
* **Objective Function:** Minimize the total cost of recycling and waste disposal operations.
* **Constraints:** Recycling facility capacities, exact waste generation amounts, and minimum sustainability thresholds.
* **Solver:** PuLP library is used to execute the Simplex algorithm for optimal routing of textile by-products (Cotton, Polyester, Blends).

## Repository Structure
* `optimization_model.py`: The main script containing the mathematical model, constraints, and solver logic.
* `requirements.txt`: Project dependencies.
* `mock_data/`: (Simulated) Sample datasets representing typical SME monthly waste generation.

## Future Scope
* Integration of a graphical user interface (GUI) for non-technical SME managers.
* Dynamic API connectivity with ERP systems (e.g., SAP, Jira Assets).
