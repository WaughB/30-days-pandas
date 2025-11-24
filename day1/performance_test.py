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
    
    module_name = "595_big-countries"
    file_path = os.path.join(current_dir, "595_big-countries.py")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    big_countries = module.big_countries
except Exception as e:
    print(f"Error importing function: {e}")
    exit(1)

def generate_data(num_rows: int) -> pd.DataFrame:
    """Generates large dataset for testing."""
    print(f"Generating {num_rows} rows of world data...")
    
    continents = ["Asia", "Europe", "Africa", "North America", "South America", "Oceania", "Antarctica"]
    
    data = {
        'name': [f"Country_{i}" for i in range(num_rows)],
        'continent': np.random.choice(continents, num_rows),
        'area': np.random.randint(1000, 5000000, num_rows),
        'population': np.random.randint(100000, 50000000, num_rows),
        'gdp': np.random.randint(1000000, 1000000000, num_rows)
    }
    
    world = pd.DataFrame(data).astype({
        "name": "object",
        "continent": "object",
        "area": "Int64",
        "population": "Int64",
        "gdp": "Int64",
    })
    
    return world

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
    world = generate_data(N_ROWS)
    
    print("\nStarting Tests...\n")
    profile_performance(big_countries, world)

if __name__ == "__main__":
    run_tests()
