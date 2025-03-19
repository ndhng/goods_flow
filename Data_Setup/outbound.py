import os
import pandas as pd
from random import choices, choice, randint

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                             number_of_outbounds, outbound_frequency,
                             max_no_outbound_days, combined_SO_frequency)

# Initialize moving constants
current_date = start_date
current_SO_number = 1
current_SO_item_number = 1

outbounds = []
for i in range(number_of_outbounds):

    # New date?
    if choices([True,False], [outbound_frequency, 1 - outbound_frequency])[0]:
        current_date = current_date + pd.DateOffset(days = randint(1,max_no_outbound_days))

    # New SO?
    if choices([True,False], [combined_SO_frequency, 1 - combined_SO_frequency])[0]:
        current_SO_number += 1
        current_SO_item_number = 1

    zeros = "0"*(3-len(str(current_SO_number)))
    SO_number = 'SO' + zeros + str(current_SO_number)

    SO_item_number = SO_number + '-' + str(current_SO_item_number)
    current_SO_item_number += 1

    # Select a random Item & Warehouse for outbound
    item_code = choice(item_codes)
    warehouse_code = choice(warehouse_codes)

    # Add all to outbound list
    outbounds.append([SO_item_number, SO_number, current_date, warehouse_code, item_code, randint(1,100)*10])

df = pd.DataFrame(outbounds, columns = ["Element_Code","Element_Number","Date","Warehouse_Code","Item_Code","Amount"])
df["Date"] = pd.to_datetime(df["Date"])

# print(df)

os.makedirs('../Datasets', exist_ok=True)
df.to_csv('../Datasets/Outbound.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Outbound.csv')
    print(test)