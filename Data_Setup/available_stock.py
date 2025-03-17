import os
import pandas as pd
from random import randint

from init import item_codes, warehouse_codes, start_date

# Initialize how many days of historical stock is saved in this file
number_of_days_history = 10

# Create the list of dates that will be included in this file
dates = []
for i in range(number_of_days_history):
    dates.append(start_date - pd.Timedelta(days=i+1))

# print(item_codes)
# print(warehouse_codes)
# print(dates)

dataset = []

for date in dates:
    for warehouse in warehouse_codes:
        for item in item_codes:
            dataset.append([date, warehouse, item, randint(1,100)*100])

df = pd.DataFrame(dataset, columns=['Date', 'Warehouse_Code', 'Item_Code', 'Stock_Amount'])
df['Date'] = pd.to_datetime(df['Date'])

# print(df)

os.makedirs('../Datasets', exist_ok=True)
df.to_csv('../Datasets/Available_Stock.csv', index=False)

test = pd.read_csv('../Datasets/Available_Stock.csv')
print(test)