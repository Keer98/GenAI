import pandas as pd
from collections import defaultdict

# Load the dataset from the CSV file
flights_df = pd.read_csv('FlightsDataset.csv')

# Create a graph from the dataset
graph = defaultdict(list)
for index, row in flights_df.iterrows():
    graph[row['Source']].append(row['Destination'])

def dfs_all_paths(graph, current, destination, path, all_paths):
    path.append(current)
    
    if current == destination:
        all_paths.append(list(path))  # Append a copy of the path to all_paths
    else:
        for neighbor in graph[current]:
            if neighbor not in path:  # Prevent cycles
                dfs_all_paths(graph, neighbor, destination, path, all_paths)
    
    path.pop()  # Backtrack

# User input for source and destination
source = input("Enter the source city: ")
destination = input("Enter the destination city: ")

# Find all paths
all_paths = []
dfs_all_paths(graph, source, destination, [], all_paths)

# Sort paths by number of stops (length of the path - 1)
sorted_paths = sorted(all_paths, key=lambda x: len(x) - 1)
limited_paths = sorted_paths[:5]
# Output the results
if limited_paths:
    print(f"All possible paths from {source} to {destination}, sorted by number of stops:")
    for path in limited_paths:
        stops = len(path) - 2  # stops are 2 less than the number of cities in the path
        print(f"Path: {' -> '.join(path)} with {stops} stop(s).")
else:
    print(f"No path found from {source} to {destination}.")
