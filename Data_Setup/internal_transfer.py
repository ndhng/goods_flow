import os
import pandas as pd
from random import choices, randint, choice

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                  number_of_transfers,
                  internal_transfer_days,
                  transfer_frequency,
                  combined_IT_frequency,
                  max_no_IT_days)

# Initialize moving constants
current_date = start_date
current_IT_number = 1
current_IT_item_number = 1

transfers = []
for i in range(number_of_transfers):

    # New date?
    if choices([True, False], [transfer_frequency, 1-transfer_frequency])[0]:
        current_date = current_date + pd.DateOffset(days=randint(1, max_no_IT_days))

    # Arrival date
    arrival_date = current_date + pd.DateOffset(days=randint(0, internal_transfer_days))

    # New IT?
    if choices([True, False], [combined_IT_frequency, 1-combined_IT_frequency])[0]:
        current_IT_number += 1
        current_IT_item_number = 1

    zeros = "0"*(3-len(str(current_IT_number)))
    IT_number = "IT" + zeros + str(current_IT_number)

    IT_item_number = IT_number + '-' + str(current_IT_item_number)
    current_IT_item_number += 1

    # Choose the 2 warehouses the goods are transferred between
    warehouse_from = choice(warehouse_codes)
    possible_destination = warehouse_codes.copy()
    possible_destination.remove(warehouse_from)
    warehouse_to = choice(possible_destination)

    # Select a random item to be transferred
    item_code = choice(item_codes)

    transfers.append([IT_item_number, IT_number,
                      current_date, warehouse_from,
                      arrival_date, warehouse_to,
                      item_code, randint(1, 50) * 10])

df = pd.DataFrame(transfers, columns=['Element_Code', 'Element_Number',
                                      'Date_Origin', 'Warehouse_Origin',
                                      'Date_Arrival', 'Warehouse_Destination',
                                      'Item_Code', 'Amount'])
df["Date_Origin"] = pd.to_datetime(df["Date_Origin"])
df["Date_Arrival"] = pd.to_datetime(df["Date_Arrival"])

# print(df)

os.makedirs('../Datasets', exist_ok=True)
df.to_csv('../Datasets/Internal_Transfers.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Internal_Transfers.csv')
    print(test)