import pandas as pd
from random import choice, randint

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                             number_of_outbounds, outbound_frequency,
                             max_no_outbound_days, combined_SO_frequency)
from Data_Setup.shared_func import next_date, generate_code_item

# Initialize moving constants
current_date = start_date
current_SO_number = 1
current_SO_item_number = 1

outbounds = []
for i in range(number_of_outbounds):

    move = next_date(outbound_frequency, max_no_outbound_days)
    current_date = current_date + pd.Timedelta(days=move)

    SO_item_number, SO_number, current_SO_number, current_SO_item_number = generate_code_item("SO", 3,
                                                                                              current_SO_number,
                                                                                              current_SO_item_number,
                                                                                              combined_SO_frequency)

    # Select a random Item & Warehouse for outbound
    item_code = choice(item_codes)
    warehouse_code = choice(warehouse_codes)

    # Add all to outbound list
    outbounds.append([SO_item_number, SO_number, current_date, warehouse_code, item_code, randint(1,100)*10])

df = pd.DataFrame(outbounds, columns = ["Element_Code","Element_Number","Date","Warehouse_Code","Item_Code","Amount"])
df["Date"] = pd.to_datetime(df["Date"])

# print(df)

df.to_csv('../Datasets/Outbound.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Outbound.csv')
    print(test)