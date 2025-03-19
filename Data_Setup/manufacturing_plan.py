from random import randint, choice, choices
import pandas as pd

from Data_Setup.manufacturing_requirements import manufacturing_requirements
from Data_Setup.init import (warehouse_codes, number_of_production_orders, start_date,
                             manufacturing_frequency, max_no_production_days, max_production_period)

manu_req_index = manufacturing_requirements.shape[0]

production_orders = []
current_date = start_date
production_order_code_number = 1

for i in range(number_of_production_orders):
    production_order_code = 'PrO' + "0"*(3-len(str(production_order_code_number))) + str(production_order_code_number)
    production_order_code_number += 1

    manu_index = randint(0, manu_req_index - 1)
    row = manufacturing_requirements.iloc[manu_index]

    manu_input = row['Input_Code']
    output = row['Output_Code']

    warehouse = choice(warehouse_codes)

    mult = randint(1, 10)
    input_weight = row['Input_Weight']*mult
    output_weight = row['Output_Weight']*mult

    if choices([True, False], [manufacturing_frequency, 1-manufacturing_frequency])[0]:
        current_date = current_date + pd.DateOffset(days=randint(1, max_no_production_days))

    finished_date = current_date + pd.DateOffset(days=randint(0, max_production_period))

    production_orders.append([production_order_code,warehouse, manu_input, input_weight, current_date, output, output_weight, finished_date])

df = pd.DataFrame(production_orders, columns=['Production_Order_Code','Warehouse', 'Input', 'Input_Weight', 'Input_Date', 'Output', 'Output_Weight', 'Output_Date'])
df['Input_Date'] = pd.to_datetime(df['Input_Date'])
df['Output_Date'] = pd.to_datetime(df['Output_Date'])

df.to_csv('../Datasets/Manufacturing_Plan.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Manufacturing_Plan.csv')
    print(test)