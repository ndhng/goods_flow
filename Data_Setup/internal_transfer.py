import pandas as pd
from random import randint, choice

from Data_Setup.init import (item_codes, warehouse_codes, start_date,
                             number_of_transfers,
                             internal_transfer_days,
                             transfer_frequency,
                             combined_IT_frequency,
                             max_no_IT_days)
from Data_Setup.shared_func import next_date, generate_code_item


def generate_internal_transfers(num_transfers=None, output_path='../Datasets/Internal_Transfers.csv'):
    """
    Generate internal transfer data and save it to a CSV file.

    Parameters:
    -----------
    num_transfers : int, optional
        Number of internal transfers to generate. If None, uses the value from init.
    output_path : str, optional
        Path where the CSV file will be saved.

    Returns:
    --------
    pandas.DataFrame
        The generated internal transfer data.
    """
    # Use the value from init if not specified
    if num_transfers is None:
        num_transfers = number_of_transfers

    # Initialize moving constants
    current_date = start_date
    current_IT_number = 1
    current_IT_item_number = 1

    transfers = []
    for i in range(num_transfers):
        move = next_date(transfer_frequency, max_no_IT_days)
        current_date = current_date + pd.Timedelta(days=move)

        arrival_date = current_date + pd.DateOffset(days=randint(0, internal_transfer_days))

        IT_item_number, IT_number, current_IT_number, current_IT_item_number = generate_code_item(
            "IT", 3, current_IT_number, current_IT_item_number, combined_IT_frequency
        )

        # Choose the 2 warehouses the goods are transferred between
        warehouse_from = choice(warehouse_codes)
        possible_destination = warehouse_codes.copy()
        possible_destination.remove(warehouse_from)
        warehouse_to = choice(possible_destination)

        # Select a random item to be transferred
        item_code = choice(item_codes)

        transfers.append([
            IT_item_number, IT_number,
            current_date, warehouse_from,
            arrival_date, warehouse_to,
            item_code, randint(1, 50) * 10
        ])

    df = pd.DataFrame(transfers, columns=[
        'Element_Code', 'Element_Number',
        'Date_Origin', 'Warehouse_Origin',
        'Date_Arrival', 'Warehouse_Destination',
        'Item_Code', 'Amount'
    ])
    df["Date_Origin"] = pd.to_datetime(df["Date_Origin"])
    df["Date_Arrival"] = pd.to_datetime(df["Date_Arrival"])

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    # When run directly, generate the internal transfer data and print it
    df = generate_internal_transfers()
    test = pd.read_csv('../Datasets/Internal_Transfers.csv')
    print(test)
