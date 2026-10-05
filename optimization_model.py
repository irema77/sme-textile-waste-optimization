import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import logging

# Configure logging for professional output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_simulated_data():
    """
    Simulates the data extraction process from an SME's ERP/Database system.
    In production, this would be replaced with a SQL/PostgreSQL query.
    """
    logging.info("Loading waste generation data for the current period...")
    data = {
        'Waste_Type': ['Cotton', 'Polyester', 'Blend_Fabric', 'Nylon'],
        'Amount_kg': [1200, 850, 600, 300],
        'Recycle_Cost_per_kg': [2.5, 3.0, 4.5, 5.0],
        'Disposal_Cost_per_kg': [4.0, 5.5, 6.0, 7.5],
        'Recycle_Capacity_kg': [1000, 1000, 400, 200]
    }
    return pd.DataFrame(data)

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
    waste_data = load_simulated_data()
    optimal_model, r_vars, d_vars = run_optimization(waste_data)
    generate_report(waste_data, optimal_model, r_vars, d_vars)
