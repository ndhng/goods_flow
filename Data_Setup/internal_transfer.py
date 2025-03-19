import pandas as pd
from random import randint, choice

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                  number_of_transfers,
                  internal_transfer_days,
                  transfer_frequency,
                  combined_IT_frequency,
                  max_no_IT_days)
from Data_Setup.shared_func import next_date, generate_code_item

# Initialize moving constants
current_date = start_date
current_IT_number = 1
current_IT_item_number = 1

transfers = []
for i in range(number_of_transfers):

    move = next_date(transfer_frequency, max_no_IT_days)
    current_date = current_date + pd.Timedelta(days=move)

    arrival_date = current_date + pd.DateOffset(days=randint(0, internal_transfer_days))

    IT_item_number, IT_number, current_IT_number, current_IT_item_number = generate_code_item("IT", 3, current_IT_number, current_IT_item_number, combined_IT_frequency)

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

df.to_csv('../Datasets/Internal_Transfers.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Internal_Transfers.csv')
    print(test)