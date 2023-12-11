#!/usr/bin/env python
# coding: utf-8

# # Task2

# ## Question 1: Distance Matrix Calculation

# In[4]:


import pandas as pd
import numpy as np
import networkx as nx


# In[5]:


df2=pd.read_csv(r"C:\Users\HP\Downloads\dataset-3.csv")


# In[7]:


def calculate_distance_matrix(df2):
    
    # Create a directed graph using networkx
    G = nx.DiGraph()

    # Add edges with distances to the graph
    for _, row in df2.iterrows():
        G.add_edge(row['id_start'], row['id_end'], weight=row['distance'])

    # Calculate the shortest paths between nodes
    all_pairs_shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G))

    # Create a DataFrame to store distances between IDs
    ids = sorted(set(df2['id_start'].unique()) | set(df2['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=ids, columns=ids)

    # Fill the distance matrix with cumulative distances
    for source in ids:
        for destination in ids:
            if source == destination:
                distance_matrix.at[source, destination] = 0
            elif destination in all_pairs_shortest_paths[source]:
                distance_matrix.at[source, destination] = all_pairs_shortest_paths[source][destination]
            else:
                # If there is no direct route, set distance to NaN
                distance_matrix.at[source, destination] = float('nan')

    return distance_matrix

result_distance_matrix = calculate_distance_matrix(df2)
result_distance_matrix.fillna(0, inplace=True)
# Display the resulting distance matrix
print(result_distance_matrix)


# ## Question 2: Unroll Distance Matrix

# In[8]:


import pandas as pd

def unroll_distance_matrix(distance_matrix):
    # Create lists to store unrolled data
    id_start_list = []
    id_end_list = []
    distance_list = []

    # Iterate over the distance matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                # Append values to lists
                id_start_list.append(id_start)
                id_end_list.append(id_end)
                distance_list.append(distance_matrix.at[id_start, id_end])

    # Create a DataFrame from the lists
    unrolled_df = pd.DataFrame({'id_start': id_start_list, 'id_end': id_end_list, 'distance': distance_list})

    return unrolled_df

result_unrolled_df = unroll_distance_matrix(result_distance_matrix)


print(result_unrolled_df)


# ## Question 3: Finding IDs within Percentage Threshold

# In[9]:


def find_ids_within_ten_percentage_threshold(result_unrolled_df, reference_value):
    # Filter the DataFrame based on the reference value
    reference_df = df2[df2['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_average_distance = reference_df['distance'].mean()

    # Calculate the lower and upper thresholds (within 10%)
    lower_threshold = reference_average_distance * 0.9
    upper_threshold = reference_average_distance * 1.1

    # Filter the DataFrame based on the thresholds
    filtered_df = df2[(df2['distance'] >= lower_threshold) & (df2['distance'] <= upper_threshold)]

    # Get the sorted list of unique id_start values within the threshold
    result_ids = sorted(filtered_df['id_start'].unique())

    return result_ids

reference_value = df2['id_start'] 
result_within_threshold = find_ids_within_ten_percentage_threshold(df2, reference_value)

print(result_within_threshold)


# ## Question 4: Calculate Toll Rate

# In[13]:


import pandas as pd

def calculate_toll_rate(result_within_threshold):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Iterate over vehicle types and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_toll'  # Define the column name
        df2[column_name] = df2['distance'] * rate_coefficient  # Calculate toll rate

    return df2

result_with_toll_rates = calculate_toll_rate(result_unrolled_df)

# Display the resulting DataFrame with toll rates
print(result_with_toll_rates)


# ## Question 5: Calculate Time-Based Toll Rates

# In[15]:


def calculate_time_based_toll_rates(df2):
    df2['start_time'] = pd.to_datetime(df2['start_time'])
    df2['end_time'] = pd.to_datetime(df2['end_time'])
    weekday_morning = pd.to_datetime('10:00:00').time()
    weekday_evening = pd.to_datetime('18:00:00').time()
    def apply_discount(row):
        if row['start_time'].weekday() < 5:  # Weekdays (Monday - Friday)
            if row['start_time'].time() < weekday_morning:
                return row * 0.8
            elif row['start_time'].time() < weekday_evening:
                return row * 1.2
            else:
                return row * 0.8
        else: 
            return row * 0.7
    vehicles = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle in vehicles:
        df2[vehicle] = df2[vehicle].apply(apply_discount)
    days_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df2['start_day'] = df2['start_time'].dt.weekday.map(days_of_week)
    df2['end_day'] = df2['end_time'].dt.weekday.map(days_of_week)
    df2['start_time'] = df2['start_time'].dt.time
    df2['end_time'] = df2['end_time'].dt.time
    return df2


# In[ ]:




