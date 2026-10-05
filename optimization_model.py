import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import logging
import os

# Configure logging for professional output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """
    Loads the simulated waste generation data from a CSV file.
    In a real SME environment, this connects to an ERP database.
    """
    logging.info(f"Loading waste generation data from {file_path}...")
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path)

def run_optimization(df):
    """
    Core linear programming model to minimize waste management costs.
    """
    logging.info("Initializing the Linear Programming model...")
    model = LpProblem("Textile_Waste_Cost_Minimization", LpMinimize)
    
    # Decision Variables
    recycle_vars = [LpVariable(f"Recycle_{row['Waste_Type']}", lowBound=0) for _, row in df.iterrows()]
    dispose_vars = [LpVariable(f"Dispose_{row['Waste_Type']}", lowBound=0) for _, row in df.iterrows()]
    
    # Objective Function
    model += lpSum([recycle_vars[i] * df.loc[i, 'Recycle_Cost_per_kg'] + 
                    dispose_vars[i] * df.loc[i, 'Disposal_Cost_per_kg'] for i in range(len(df))])
    
    # Constraints
    logging.info("Applying capacity and flow constraints...")
    for i in range(len(df)):
        # 1. Total waste must be processed
        model += recycle_vars[i] + dispose_vars[i] == df.loc[i, 'Amount_kg']
        # 2. Cannot exceed recycling facility capacities
        model += recycle_vars[i] <= df.loc[i, 'Recycle_Capacity_kg']
        
    # Solve
    logging.info("Executing Simplex algorithm via PuLP...")
    model.solve()
    
    return model, recycle_vars, dispose_vars

def generate_report(df, model, recycle_vars, dispose_vars):
    """
    Generates a structured report of the decision variables.
    """
    print("\n" + "="*50)
    print(" DSS OPTIMIZATION RESULTS ".center(50, "="))
    print("="*50)
    
    for i, row in df.iterrows():
        print(f"Material: {row['Waste_Type']}")
        print(f"  -> Send to Recycling: {recycle_vars[i].varValue} kg")
        print(f"  -> Send to Disposal:  {dispose_vars[i].varValue} kg")
        print("-" * 50)
        
    print(f"OPTIMIZED TOTAL COST: ₺{value(model.objective):,.2f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    # Updated to read from the mock_data directory
    data_path = "mock_data/waste_data.csv"
    waste_data = load_data(data_path)
    optimal_model, r_vars, d_vars = run_optimization(waste_data)
    generate_report(waste_data, optimal_model, r_vars, d_vars)
