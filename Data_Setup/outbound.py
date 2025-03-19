import pandas as pd
from random import choice, randint

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                             number_of_outbounds, outbound_frequency,
                             max_no_outbound_days, combined_SO_frequency)
from Data_Setup.shared_func import next_date, generate_code_item


def generate_outbound_data(num_outbounds=None, output_path='../Datasets/Outbound.csv'):
    """
    Generate outbound order data and save it to a CSV file.

    Parameters:
    -----------
    num_outbounds : int, optional
        Number of outbound orders to generate. If None, uses the value from init.
    output_path : str, optional
        Path where the CSV file will be saved.

    Returns:
    --------
    pandas.DataFrame
        The generated outbound data.
    """
    # Use the value from init if not specified
    if num_outbounds is None:
        num_outbounds = number_of_outbounds

    # Initialize moving constants
    current_date = start_date
    current_SO_number = 1
    current_SO_item_number = 1

    outbounds = []
    for i in range(num_outbounds):
        move = next_date(outbound_frequency, max_no_outbound_days)
        current_date = current_date + pd.Timedelta(days=move)

        SO_item_number, SO_number, current_SO_number, current_SO_item_number = generate_code_item(
            "SO", 3,
            current_SO_number,
            current_SO_item_number,
            combined_SO_frequency
        )

        # Select a random Item & Warehouse for outbound
        item_code = choice(item_codes)
        warehouse_code = choice(warehouse_codes)

        # Add all to outbound list
        outbounds.append([
            SO_item_number,
            SO_number,
            current_date,
            warehouse_code,
            item_code,
            randint(1, 100) * 10
        ])

    df = pd.DataFrame(outbounds, columns=[
        "Element_Code",
        "Element_Number",
        "Date",
        "Warehouse_Code",
        "Item_Code",
        "Amount"
    ])
    df["Date"] = pd.to_datetime(df["Date"])

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    # When run directly, generate the outbound data and print it
    df = generate_outbound_data()
    test = pd.read_csv('../Datasets/Outbound.csv')
    print(test)
