import pandas as pd

data = [[1, 'Joe'], [2, 'Henry'], [3, 'Sam'], [4, 'Max']]
customers = pd.DataFrame(data, columns=['id', 'name']).astype({'id':'Int64', 'name':'object'})
data = [[1, 3], [2, 1]]
orders = pd.DataFrame(data, columns=['id', 'customerId']).astype({'id':'Int64', 'customerId':'Int64'})

# Function to find customers who are in the customers table but not in the orders table.
# Output needs to be a table with only the customer names remainig titled "Customers".
def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:

    return customers[~customers['id'].isin(orders['customerId'])][['name']].rename(columns={'name': 'Customers'})

## Second method.
def find_customers_2(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    
    merged = customers.merge(orders, left_on='id', right_on='customerId', how='left')
    result = merged[merged['customerId'].isna()][['name']].rename(columns={'name': 'Customers'})

    return result


print("First method\n", find_customers(customers, orders))
print("Second method\n", find_customers(customers, orders))