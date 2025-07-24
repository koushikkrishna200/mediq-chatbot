import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

def preprocess_query(query):
    """
    Preprocess the query text by converting to lowercase, removing non-alphanumeric characters, and stripping extra spaces.
    
    :param query: The query string to preprocess.
    :return: Cleaned query string.
    """
    query = query.lower()  # Convert to lowercase
    query = re.sub(r'\s+', ' ', query)  # Remove extra spaces
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)  # Remove non-alphanumeric characters
    return query

def visualize_most_common_queries(query_data):
    """
    Visualize the most common queries using a bar plot.
    
    :param query_data: A list of queries that have been logged.
    """
    # Count the occurrences of each query
    query_counts = Counter(query_data)

    # Convert the counts to a DataFrame for better visualization
    query_df = pd.DataFrame(query_counts.items(), columns=["Query", "Count"])
    query_df = query_df.sort_values(by="Count", ascending=False)

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Count", y="Query", data=query_df.head(10), palette="viridis")

    plt.title("Top 10 Most Common Medical Queries")
    plt.xlabel("Query Count")
    plt.ylabel("Query")
    plt.tight_layout()  # Ensure labels are not cut off
    plt.show()

def load_query_data(file_path="queries_log.csv"):
    """
    Load the query data from a CSV file where queries are logged.
    
    :param file_path: The path to the file containing logged queries.
    :return: A list of queries.
    """
    try:
        # Load the CSV containing the logged queries
        df = pd.read_csv(file_path)
        
        # Preprocess queries
        df["query"] = df["query"].apply(preprocess_query)
        
        return df["query"].tolist()
    except FileNotFoundError:
        print(f"File {file_path} not found. No query data to visualize.")
        return []
    except Exception as e:
        print(f"Error loading the query data: {e}")
        return []

if __name__ == "__main__":
    # Example usage of the visualization function
    queries = load_query_data("queries_log.csv")  # You can change the path as needed
    if queries:
        visualize_most_common_queries(queries)
