import pandas as pd
from datetime import datetime
import os

def log_query(query, file_path="queries_log.csv"):
    """
    Logs the query to a CSV file.
    
    :param query: The query string to log.
    :param file_path: The path to the file where queries will be logged.
    """
    # Prepare data to be logged
    data = {
        "timestamp": [datetime.now().isoformat()],  # ISO format timestamp
        "query": [query]
    }
    
    df = pd.DataFrame(data)
    
    # Check if the file already exists to avoid writing headers every time
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, mode="w", header=True, index=False)

def get_top_queries(file_path="queries_log.csv", top_n=10):
    """
    Retrieves the top N most frequent queries from the CSV log file.
    
    :param file_path: The path to the file where queries are logged.
    :param top_n: The number of top queries to return.
    :return: A pandas Series with the top N queries.
    """
    # Read the CSV file
    if os.path.exists(file_path):
        query_log = pd.read_csv(file_path)
        return query_log['query'].value_counts().head(top_n)
    else:
        return pd.Series([])  # Return empty series if no queries are logged

# Example usage:
log_query("What is diabetes?")
log_query("How to manage hypertension?")
log_query("What is diabetes?")

# Get top queries
top_queries = get_top_queries()
print(top_queries)
