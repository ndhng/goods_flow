import pandas as pd
from random import choice, randint

from init import (item_codes, warehouse_codes, start_date,
                  number_of_inbounds, inbound_frequency,
                  max_no_inbound_days, combined_PO_frequency)
from Data_Setup.shared_func import next_date, generate_code_item


def generate_inbound_data(num_inbounds=None, output_path='./Datasets/Inbound.csv'):
    """
    Generate inbound data and save it to a CSV file.

    Parameters:
    -----------
    num_inbounds : int, optional
        Number of inbound records to generate. If None, uses the value from init.
    output_path : str, optional
        Path where the CSV file will be saved.

    Returns:
    --------
    pandas.DataFrame
        The generated inbound data.
    """
    # Use the value from init if not specified
    if num_inbounds is None:
        num_inbounds = number_of_inbounds

    # Initialize moving constants
    current_date = start_date
    current_PO_number = 1
    current_PO_item_number = 1

    inbounds = []
    for i in range(num_inbounds):
        move = next_date(inbound_frequency, max_no_inbound_days)
        current_date = current_date + pd.Timedelta(days=move)

        PO_item_number, PO_number, current_PO_number, current_PO_item_number = generate_code_item(
            "PO", 3, current_PO_number, current_PO_item_number, combined_PO_frequency
        )

        # Select a random Item & Warehouse for inbound
        item_code = choice(item_codes)
        warehouse_code = choice(warehouse_codes)

        # Add all to inbound list
        inbounds.append([
            PO_item_number,
            PO_number,
            current_date,
            warehouse_code,
            item_code,
            randint(1, 100) * 10
        ])

    df = pd.DataFrame(inbounds, columns=[
        "Element_Code", "Element_Number", "Date",
        "Warehouse_Code", "Item_Code", "Amount"
    ])
    df["Date"] = pd.to_datetime(df["Date"])

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    # When run directly, generate the inbound data and print it
    df = generate_inbound_data()
    test = pd.read_csv('./Datasets/Inbound.csv')
    print(test)
