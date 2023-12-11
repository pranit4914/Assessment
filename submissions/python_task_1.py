#!/usr/bin/env python
# coding: utf-8

# In[39]:


import pandas as pd
import numpy as np


# In[40]:


df=pd.read_csv(r"C:\Users\HP\Downloads\dataset-1.csv")


# # Task 1

# ## Question 1: Car Matrix Generation

# In[99]:


def generate_car_matrix(data):
    result_df = data.pivot(index='id_1', columns='id_2', values='car')
    result_df.fillna(0, inplace=True)  
    result_df.values[[range(len(result_df))], [range(len(result_df))]] = 0   
    return result_df
new_df = generate_car_matrix(df)
print(new_df)


# ## Question 2: Car Type Count Calculation

# In[100]:


import pandas as pd

def get_type_count(df):
    
    # Add a new 'car_type' column based on the specified conditions
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

result = get_type_count(df)

print(result)


# ## Question 3: Bus Count Index Retrieval

# In[101]:


import pandas as pd

def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where the 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

result_indexes = get_bus_indexes(df)

print(result_indexes)


# ## Question 4: Route Filtering

# In[102]:


def filter_routes(df):

    # Group by 'route' and calculate the average of the 'truck' column for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

result_routes = filter_routes(df)

print(result_routes)


# ## Question 5: Matrix Value Modification

# In[103]:


def multiply_matrix(result_matrix):
    # Copy the input DataFrame to avoid modifying the original
    modified_matrix = result_matrix.copy()

    # Apply the specified logic to modify the values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

result_matrix = generate_car_matrix(df)

# Call the multiply_matrix function
modified_result_matrix = multiply_matrix(result_matrix)

print(modified_result_matrix)


# ## Question 6: Time Check

# In[104]:


df1=pd.read_csv(r"C:\Users\HP\Downloads\dataset-2.csv")


# In[106]:


import pandas as pd

def check_timestamps(df1):
    # Combine date and time columns to create datetime objects
    df1['start_datetime'] = pd.to_datetime(df1['startDay'] + ' ' + df1['startTime'], format='%A %H:%M:%S')
    df1['end_datetime'] = pd.to_datetime(df1['endDay'] + ' ' + df1['endTime'], format='%A %H:%M:%S')

    # Check if the timestamps cover a full 24-hour period and span all 7 days
    df1['valid_timestamp'] = (
        (df1['start_datetime'].dt.time == pd.to_datetime('00:00:00').time()) &
        (df1['end_datetime'].dt.time == pd.to_datetime('23:59:59').time()) &
        (df1['start_datetime'].dt.dayofweek.isin([0, 1, 2, 3, 4, 5, 6])) &
        (df1['end_datetime'].dt.dayofweek.isin([0, 1, 2, 3, 4, 5, 6]))
    )

    # Create a multi-index with (id, id_2)
    multi_index = df1.set_index(['id', 'id_2']).index

    # Extract the boolean series with multi-index
    result_series = df1['valid_timestamp'].groupby(multi_index).any()

    return result_series

result_series = check_timestamps(df1)

print(result_series)

