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
    
    module_name = "1148_article-views-1"
    file_path = os.path.join(current_dir, "1148_article-views-1.py")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    article_views = module.article_views
except Exception as e:
    print(f"Error importing function: {e}")
    exit(1)

def generate_data(num_rows: int) -> pd.DataFrame:
    """Generates large dataset for testing."""
    print(f"Generating {num_rows} views...")
    
    # Generate random IDs
    article_ids = np.random.randint(1, 1000, num_rows)
    author_ids = np.random.randint(1, 500, num_rows)
    viewer_ids = np.random.randint(1, 500, num_rows)
    
    # Ensure some authors view their own articles (approx 10%)
    mask = np.random.random(num_rows) < 0.1
    viewer_ids[mask] = author_ids[mask]
    
    # Generate dates
    dates = pd.date_range(start='2023-01-01', periods=100).to_list()
    view_dates = np.random.choice(dates, num_rows)
    
    views = pd.DataFrame({
        'article_id': article_ids,
        'author_id': author_ids,
        'viewer_id': viewer_ids,
        'view_date': view_dates
    }).astype({
        'article_id': 'Int64',
        'author_id': 'Int64',
        'viewer_id': 'Int64',
        'view_date': 'datetime64[ns]'
    })
    
    return views

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
    views = generate_data(N_ROWS)
    
    print("\nStarting Tests...\n")
    profile_performance(article_views, views)

if __name__ == "__main__":
    run_tests()
