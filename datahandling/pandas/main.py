from io import StringIO

import pandas as pd

data=StringIO("""
Id;Value A;Value B;Value C;Quantity;Valid
1;12;5;7;5;YES
2;13;7;7;18;YES
3;14;8;8;12;NO
4;15;9;9;23;NO
5;16;7;5;46;NO
""")

# Get the IDs for the rows that have the sum of Value B and Value C greater than Value A and have the column Valid set to YES
# Calculate the sum of the quantity column for the IDs selected above

df = pd.read_csv(data, delimiter=";")
df.info()
df.describe()
df.head()


# Data Filtering
df['result']=df.apply(
    lambda row: 1 if (row['Value B']+row['Value C']>row['Value A']) and (row['Valid']=='YES') else 0,
    axis=1,
)
list(df[df.result==1].Id)


# Grouping Data

## Example 1: Basic aggregation
grouped_basic = df.groupby('Valid').sum()
print("Basic Aggregation:\n", grouped_basic)

## Example 2: Custom aggregation function
grouped_custom = df.groupby('Valid').agg({'Quantity': 'sum', 'Value A': 'mean'})
print("Custom Aggregation Function:\n", grouped_custom)

def my_custom_function(x):
    return x.max() - x.min()

grouped_custom_function = df.groupby('Valid').agg({'Quantity': my_custom_function, 'Value A': 'mean'})

## Example 3: Named aggregation
grouped_named = df.groupby('Valid').agg(
    total_quantity=pd.NamedAgg(column='Quantity', aggfunc='sum'),
    average_value_a=pd.NamedAgg(column='Value A', aggfunc='mean')
)
print("Named Aggregation:\n", grouped_named)