from io import StringIO

import pandas as pd

data=StringIO("""
Id;Value A;Value B;Value C;Quantity;Valid
1;12;5;7;5;YES
2;13;7;7;18;YES
3;14;8;8;12;NO
4;15;9;9;23;NO
5;16;7;5;46;NO
6;17;7;7;6;YES
7;18;8;8;4;NO
8;19;9;9;8;NO
9;20;10;15;5;NO
10;21;11;11;90;YES
""")

# Get the IDs for the rows that have the sum of Value B and Value C greater than Value A and have the column Valid set to YES
# Calculate the sum of the quantity column for the IDs selected above

df = pd.read_csv(data, delimiter=";")
df.info()

df['result']=df.apply(lambda row: 1 if (row['Value B']+row['Value C']>row['Value A']) and (row['Valid']=='YES') else 0 , axis=1 )

list(df[df.result==1].Id)

df[df.result==1].Quantity.sum()