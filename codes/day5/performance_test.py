import pandas as pd
import numpy as np
import time
import tracemalloc
import sys
import os
import string

# Import the function to test
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    module_name = "1683_invalid-tweets"
    file_path = os.path.join(current_dir, "1683_invalid-tweets.py")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    invalid_tweets = module.invalid_tweets
except Exception as e:
    print(f"Error importing function: {e}")
    exit(1)

def generate_data(num_rows: int) -> pd.DataFrame:
    """Generates large dataset for testing."""
    print(f"Generating {num_rows} tweets...")
    
    tweet_ids = np.arange(1, num_rows + 1)
    
    # Generate random strings of varying lengths
    # Some short (<= 15), some long (> 15)
    
    def random_string(length):
        return ''.join(np.random.choice(list(string.ascii_letters + " "), length))
    
    # Vectorized approach for faster generation is tricky with variable lengths, 
    # so we'll just generate a list comprehension which is fast enough for 100k
    
    # 50% chance of being invalid (>15 chars)
    lengths = np.random.randint(1, 30, num_rows)
    content = [random_string(l) for l in lengths]
    
    tweets = pd.DataFrame({
        'tweet_id': tweet_ids,
        'content': content
    }).astype({
        'tweet_id': 'Int64',
        'content': 'object'
    })
    
    return tweets

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
    tweets = generate_data(N_ROWS)
    
    print("\nStarting Tests...\n")
    profile_performance(invalid_tweets, tweets)

if __name__ == "__main__":
    run_tests()
