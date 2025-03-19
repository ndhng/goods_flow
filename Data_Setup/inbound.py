import pandas as pd
from random import choice, randint

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                             number_of_inbounds, inbound_frequency,
                             max_no_inbound_days, combined_PO_frequency)
from Data_Setup.shared_func import next_date, generate_code_item

# Initialize moving constants
current_date = start_date
current_PO_number = 1
current_PO_item_number = 1

inbounds = []
for i in range(number_of_inbounds):

    move = next_date(inbound_frequency, max_no_inbound_days)
    current_date = current_date + pd.Timedelta(days=move)

    PO_item_number, PO_number, current_PO_number, current_PO_item_number = generate_code_item("PO", 3, current_PO_number, current_PO_item_number, combined_PO_frequency)

    # Select a random Item & Warehouse for inbound
    item_code = choice(item_codes)
    warehouse_code = choice(warehouse_codes)

    # Add all to inbound list
    inbounds.append([PO_item_number, PO_number, current_date, warehouse_code, item_code, randint(1,100)*10])

df = pd.DataFrame(inbounds, columns = ["Element_Code","Element_Number","Date","Warehouse_Code","Item_Code","Amount"])
df["Date"] = pd.to_datetime(df["Date"])

# print(df)

df.to_csv('../Datasets/Inbound.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Inbound.csv')
    print(test)