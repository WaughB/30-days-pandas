import pandas as pd
import numpy as np
import time
import tracemalloc
import functools
from typing import Callable, Tuple

# Import the functions to test
# Note: We might need to adjust the import depending on how the user runs this script.
# Assuming this script is in the same directory as 183_customers-never-order.py
# We will import the module dynamically or just copy the functions here for the harness if import fails,
# but let's try to import first.
try:
    from importlib.util import spec_from_file_location
    import sys
    import os
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    # Import the specific file
    module_name = "183_customers-never-order"
    file_path = os.path.join(current_dir, "183_customers-never-order.py")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    find_customers = module.find_customers
    find_customers_2 = module.find_customers_2
except Exception as e:
    print(f"Error importing functions: {e}")
    print("Please ensure 183_customers-never-order.py is in the same directory.")
    exit(1)

def generate_data(num_customers: int, num_orders: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generates large datasets for testing."""
    print(f"Generating {num_customers} customers and {num_orders} orders...")
    
    # Generate Customers
    customer_ids = np.arange(1, num_customers + 1)
    # Random names (just simple strings)
    names = [f"Customer_{i}" for i in customer_ids]
    customers = pd.DataFrame({
        'id': customer_ids,
        'name': names
    }).astype({'id': 'Int64', 'name': 'object'})
    
    # Generate Orders
    order_ids = np.arange(1, num_orders + 1)
    # Randomly assign orders to customers (some customers will have no orders)
    # Let's say only 70% of customers make orders to ensure we have "never order" customers
    active_customer_ids = np.random.choice(customer_ids, size=int(num_customers * 0.7), replace=False)
    
    # Assign random active customers to orders
    order_customer_ids = np.random.choice(active_customer_ids, size=num_orders, replace=True)
    
    orders = pd.DataFrame({
        'id': order_ids,
        'customerId': order_customer_ids
    }).astype({'id': 'Int64', 'customerId': 'Int64'})
    
    return customers, orders

def profile_performance(func: Callable, *args, **kwargs):
    """Runs a function and measures execution time and peak memory usage."""
    
    # Start memory tracking
    tracemalloc.start()
    
    start_time = time.perf_counter()
    
    # Run function
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = (end_time - start_time) * 1000 # to ms
    peak_memory_mb = peak / (1024 * 1024)
    
    print(f"--- Performance for {func.__name__} ---")
    print(f"Time:   {execution_time:.2f} ms")
    print(f"Memory: {peak_memory_mb:.2f} MB (Peak)")
    print("-" * 30)
    
    return result

def run_tests():
    # LeetCode Constraints often go up to 10^5
    N_CUSTOMERS = 100_000
    N_ORDERS = 200_000
    
    customers, orders = generate_data(N_CUSTOMERS, N_ORDERS)
    
    print("\nStarting Tests...\n")
    
    # Test Method 1 (Filtering)
    profile_performance(find_customers, customers, orders)
    
    # Test Method 2 (Merge)
    profile_performance(find_customers_2, customers, orders)

if __name__ == "__main__":
    run_tests()
