from random import randint, choice
import pandas as pd

from Data_Setup.manufacturing_requirements import generate_manufacturing_requirements
from init import (warehouse_codes, number_of_production_orders, start_date,
                  manufacturing_frequency, max_no_production_days, max_production_period)
from Data_Setup.shared_func import generate_code, next_date


def generate_manufacturing_plan(num_production_orders=None, output_path='./Datasets/Manufacturing_Plan.csv',
                                requirements_path=None):
    """
    Generate manufacturing plan data and save it to a CSV file.

    Parameters:
    -----------
    num_production_orders : int, optional
        Number of production orders to generate. If None, uses the value from init.
    output_path : str, optional
        Path where the CSV file will be saved.
    regenerate_requirements : bool, optional
        If True, regenerates manufacturing requirements before creating the plan.
    requirements_path : str, optional
        Path where to save regenerated requirements if regenerate_requirements is True.

    Returns:
    --------
    pandas.DataFrame
        The generated manufacturing plan data.
    """
    # Use the value from init if not specified
    if num_production_orders is None:
        num_production_orders = number_of_production_orders

    # Optionally regenerate requirements
    requirements_df = generate_manufacturing_requirements()

    manu_req_index = requirements_df.shape[0]

    production_orders = []
    current_date = start_date
    production_order_code_number = 1

    for i in range(num_production_orders):
        production_order_code, production_order_code_number = generate_code('PrO', 3, production_order_code_number)

        manu_index = randint(0, manu_req_index - 1)
        row = requirements_df.iloc[manu_index]

        manu_input = row['Input_Code']
        output = row['Output_Code']

        warehouse = choice(warehouse_codes)

        mult = randint(1, 10)
        input_weight = row['Input_Weight'] * mult
        output_weight = row['Output_Weight'] * mult

        move = next_date(manufacturing_frequency, max_no_production_days)
        current_date = current_date + pd.DateOffset(days=move)

        finished_date = current_date + pd.DateOffset(days=randint(0, max_production_period))

        production_orders.append([
            production_order_code,
            warehouse,
            manu_input,
            input_weight,
            current_date,
            output,
            output_weight,
            finished_date
        ])

    df = pd.DataFrame(production_orders, columns=[
        'Production_Order_Code',
        'Warehouse',
        'Input',
        'Input_Weight',
        'Input_Date',
        'Output',
        'Output_Weight',
        'Output_Date'
    ])
    df['Input_Date'] = pd.to_datetime(df['Input_Date'])
    df['Output_Date'] = pd.to_datetime(df['Output_Date'])

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    # When run directly, generate the manufacturing plan data and print it
    df = generate_manufacturing_plan()
    test = pd.read_csv('./Datasets/Manufacturing_Plan.csv')
    print(test)
