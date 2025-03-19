import pandas as pd
from random import randint

from init import item_codes, warehouse_codes, start_date


def generate_stock_table(days_history=10, output_path='./Datasets/Available_Stock.csv'):
    """
    Generate a table of available stock and save it to a CSV file.

    Parameters:
    -----------
    days_history : int
        Number of days of historical stock data to generate.
    output_path : str
        Path where the CSV file will be saved.

    Returns:
    --------
    pandas.DataFrame
        The generated stock data.
    """
    # Create the list of dates that will be included in this file
    dates = []
    for i in range(days_history):
        dates.append(start_date - pd.Timedelta(days=i + 1))

    dataset = []

    for date in dates:
        for warehouse in warehouse_codes:
            for item in item_codes:
                dataset.append([date, warehouse, item, randint(1, 100) * 100])

    df = pd.DataFrame(dataset, columns=['Date', 'Warehouse_Code', 'Item_Code', 'Stock_Amount'])
    df['Date'] = pd.to_datetime(df['Date'])

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    # When run directly, generate the stock table and print a sample
    df = generate_stock_table()
    test = pd.read_csv('./Datasets/Available_Stock.csv')
    print(test)
