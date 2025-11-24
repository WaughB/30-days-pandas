import pandas as pd
import numpy as np
import time
import tracemalloc
import sys
import os

# Import the function to test
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    module_name = "1757_recyclable-and-low-fat-products"
    file_path = os.path.join(current_dir, "1757_recyclable-and-low-fat-products.py")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    find_products = module.find_products
except Exception as e:
    print(f"Error importing function: {e}")
    exit(1)

def generate_data(num_rows: int) -> pd.DataFrame:
    """Generates large dataset for testing."""
    print(f"Generating {num_rows} products...")
    
    data = {
        'product_id': np.arange(1, num_rows + 1),
        'low_fats': np.random.choice(['Y', 'N'], num_rows),
        'recyclable': np.random.choice(['Y', 'N'], num_rows)
    }
    
    products = pd.DataFrame(data).astype({
        "product_id": "int64",
        "low_fats": "object",
        "recyclable": "object"
    })
    
    return products

def profile_performance(func, *args, **kwargs):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = (end_time - start_time) * 1000
    peak_memory_mb = peak / (1024 * 1024)
    
    print(f"--- Performance for {func.__name__} ---")
    print(f"Time:   {execution_time:.2f} ms")
    print(f"Memory: {peak_memory_mb:.2f} MB (Peak)")
    print("-" * 30)
    
    return result

def run_tests():
    N_ROWS = 100_000
    products = generate_data(N_ROWS)
    
    print("\nStarting Tests...\n")
    profile_performance(find_products, products)

if __name__ == "__main__":
    run_tests()
