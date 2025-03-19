import os
import pandas as pd
from random import choices, choice, randint

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                             number_of_inbounds, inbound_frequency,
                             max_no_inbound_days, combined_PO_frequency)

# Initialize moving constants
current_date = start_date
current_PO_number = 1
current_PO_item_number = 1

inbounds = []
for i in range(number_of_inbounds):

    # New date?
    if choices([True,False], [inbound_frequency, 1 - inbound_frequency])[0]:
        current_date = current_date + pd.DateOffset(days = randint(1,max_no_inbound_days))

    # New PO?
    if choices([True,False], [combined_PO_frequency, 1 - combined_PO_frequency])[0]:
        current_PO_number += 1
        current_PO_item_number = 1

    zeros = "0"*(3-len(str(current_PO_number)))
    SO_number = 'SO' + zeros + str(current_PO_number)

    SO_item_number = SO_number + '-' + str(current_PO_item_number)
    current_PO_item_number += 1

    # Select a random Item & Warehouse for inbound
    item_code = choice(item_codes)
    warehouse_code = choice(warehouse_codes)

    # Add all to inbound list
    inbounds.append([SO_item_number, SO_number, current_date, warehouse_code, item_code, randint(1,100)*10])

df = pd.DataFrame(inbounds, columns = ["Element_Code","Element_Number","Date","Warehouse_Code","Item_Code","Amount"])
df["Date"] = pd.to_datetime(df["Date"])

# print(df)

os.makedirs('../Datasets', exist_ok=True)
df.to_csv('../Datasets/Inbound.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Inbound.csv')
    print(test)