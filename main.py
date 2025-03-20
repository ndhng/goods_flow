import pandas as pd
from typing import List, Tuple

from Data_Setup.available_stock import generate_stock_table
from Data_Setup.inbound import generate_inbound_data
from Data_Setup.internal_transfer import generate_internal_transfers
from Data_Setup.manufacturing_plan import generate_manufacturing_plan
from Data_Setup.outbound import generate_outbound_data

from init import warehouse_codes
import filter

from divide_input_output import separate_manufacturing_plan, separate_internal_transfer

# Constants
DATASETS_DIR = './Datasets'
DASHBOARD_OUTPUT = './Dashboard.csv'
generate_new_date = True # Replace with False to prevent constantly generating new data


def generate_all_datasets() -> None:
    """
    Generate all necessary datasets for inventory analysis.
    This includes manufacturing plans, stock tables, inbound/outbound data,
    and internal transfers.
    """
    generate_manufacturing_plan()
    generate_stock_table()
    generate_inbound_data()
    generate_internal_transfers()
    generate_outbound_data()


def load_and_filter_stock(item_filter: str, previous_date: str) -> pd.DataFrame:
    """
    Load stock data from CSV and filter by date and item code.

    Args:
        item_filter: The item code to filter data by
        previous_date: The date to filter data by (as string in YYYY-MM-DD format)

    Returns:
        DataFrame containing filtered stock data
    """
    stock_df = pd.read_csv(f'{DATASETS_DIR}/Available_Stock.csv')
    return stock_df[(stock_df['Date'] == previous_date) &
                    (stock_df['Item_Code'] == item_filter)]


def load_and_prepare_data(item_filter: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load and prepare all necessary datasets for dashboard creation.

    Args:
        item_filter: The item code to filter data by

    Returns:
        Tuple of DataFrames (inbound, outbound, manufacturing, transfers)
    """
    # Read base dataframes
    inbound_df = pd.read_csv(f'{DATASETS_DIR}/Inbound.csv')
    outbound_df = pd.read_csv(f'{DATASETS_DIR}/Outbound.csv')

    # Transform manufacturing and transfers data
    manufacturing_df = separate_manufacturing_plan()
    transfers_df = separate_internal_transfer()

    # Filter all dataframes for the specified item code
    inbound_df = inbound_df[inbound_df["Item_Code"] == item_filter]
    outbound_df = outbound_df[outbound_df["Item_Code"] == item_filter]
    manufacturing_df = manufacturing_df[manufacturing_df["Item_Code"] == item_filter]
    transfers_df = transfers_df[transfers_df["Item_Code"] == item_filter]

    return inbound_df, outbound_df, manufacturing_df, transfers_df


def prepare_dataset_copies(
        inbound_df: pd.DataFrame,
        outbound_df: pd.DataFrame,
        manufacturing_df: pd.DataFrame,
        transfers_df: pd.DataFrame,
        warehouse_codes: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Prepare copies of the datasets with standardized formats for dashboard integration.

    Args:
        inbound_df: DataFrame containing inbound data
        outbound_df: DataFrame containing outbound data
        manufacturing_df: DataFrame containing manufacturing data
        transfers_df: DataFrame containing transfers data
        warehouse_codes: List of warehouse codes to add as columns

    Returns:
        Tuple of prepared DataFrames ready for dashboard integration
    """
    # Common columns needed for the dashboard
    required_columns = ['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']

    # Prepare inbound data
    inbound_copy = inbound_df.copy()
    inbound_copy['Element_Name'] = 'Purchase Order Item'
    inbound_copy = inbound_copy[required_columns]

    # Prepare outbound data
    outbound_copy = outbound_df.copy()
    outbound_copy['Element_Name'] = 'Sales Order Item'
    outbound_copy['Amount'] = outbound_copy['Amount'] * -1
    outbound_copy = outbound_copy[required_columns]

    # Manufacturing and transfers already have correct Element_Name from separate functions
    manufacturing_copy = manufacturing_df[required_columns]
    transfers_copy = transfers_df[required_columns]

    # Add empty columns for warehouses
    for df in [inbound_copy, outbound_copy, manufacturing_copy, transfers_copy]:
        for warehouse in warehouse_codes:
            df[warehouse] = None

    return inbound_copy, outbound_copy, manufacturing_copy, transfers_copy


def create_initial_dashboard(previous_date: str, item_filter: str, stock_df: pd.DataFrame,
                             warehouse_codes: List[str]) -> pd.DataFrame:
    """
    Create the initial dashboard with the first row containing starting stock values.

    Args:
        previous_date: The date before the starting date (as string)
        item_filter: The item code being tracked
        stock_df: DataFrame containing filtered stock data
        warehouse_codes: List of warehouse codes to include

    Returns:
        Dashboard DataFrame with initial row populated
    """
    # Set up columns for dashboard
    cols = ['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']
    for warehouse in warehouse_codes:
        cols.append(warehouse)

    # Create first row with starting stock values
    first_row = [previous_date, 'Starting Stock', None, f'Item Code: {item_filter}', None, None]
    for warehouse in warehouse_codes:
        first_row.append(stock_df[stock_df['Warehouse_Code'] == warehouse]['Stock_Amount'].sum())

    # Create dashboard with first row
    dashboard = pd.DataFrame(columns=cols, index=[0])
    dashboard.iloc[0] = first_row

    return dashboard


def update_warehouse_balances(dashboard: pd.DataFrame, warehouse_codes: List[str]) -> pd.DataFrame:
    """
    Update warehouse balances in the dashboard based on transactions.
    Uses a more efficient approach than row-by-row updates.

    Args:
        dashboard: DataFrame containing the dashboard data
        warehouse_codes: List of warehouse codes to process

    Returns:
        Dashboard DataFrame with updated warehouse balances
    """
    result = dashboard.copy()

    # Process each row in sequence to maintain running balances
    for index, row in result.iterrows():
        if index == 0:
            continue

        # Get previous row values
        prev = result.loc[index - 1]

        for warehouse in warehouse_codes:
            # If this transaction affects this warehouse, add the amount to previous balance
            if warehouse == row['Warehouse_Code']:
                result.loc[index, warehouse] = prev[warehouse] + row['Amount']
            else:
                # Otherwise, carry forward the previous balance
                result.loc[index, warehouse] = prev[warehouse]

    return result


def create_dashboard(item_filter: str, warehouse_codes: List[str]) -> pd.DataFrame:
    """
    Create a complete inventory dashboard tracking item movements and warehouse balances.

    Args:
        item_filter: The item code to track
        warehouse_codes: List of warehouse codes to include

    Returns:
        Complete dashboard DataFrame
    """
    # Calculate previous date for stock reference
    previous_date = filter.starting_date - pd.DateOffset(days=1)
    previous_date_str = previous_date.strftime('%Y-%m-%d')

    # Load and filter stock data
    stock_df = load_and_filter_stock(item_filter, previous_date_str)

    # Load and prepare all datasets
    inbound_df, outbound_df, manufacturing_df, transfers_df = load_and_prepare_data(item_filter)

    # Prepare standardized copies for dashboard integration
    inbound_copy, outbound_copy, manufacturing_copy, transfers_copy = prepare_dataset_copies(
        inbound_df, outbound_df, manufacturing_df, transfers_df, warehouse_codes
    )

    # Create initial dashboard with starting stock
    dashboard = create_initial_dashboard(previous_date_str, item_filter, stock_df, warehouse_codes)

    # Combine all transaction data
    combined_df = pd.concat([inbound_copy, outbound_copy, manufacturing_copy, transfers_copy])

    # Add transactions to dashboard and sort by date
    dashboard = pd.concat([dashboard, combined_df], ignore_index=True)
    dashboard = dashboard.sort_values(by='Date', ignore_index=True)

    # Update warehouse balances
    dashboard = update_warehouse_balances(dashboard, warehouse_codes)

    return dashboard


def save_dashboard(dashboard: pd.DataFrame, output_path: str = DASHBOARD_OUTPUT) -> None:
    """
    Save the dashboard to a CSV file.

    Args:
        dashboard: DataFrame containing the dashboard data
        output_path: Path where the CSV file will be saved
    """
    dashboard.to_csv(output_path, index=False)
    print(f"Dashboard saved to {output_path}")


def main() -> None:
    """
    Main execution function for generating the inventory dashboard.
    """
    # Uncomment to regenerate all datasets
    if generate_new_date:
        generate_all_datasets()

    # Create dashboard for the filtered item across all warehouses
    dashboard = create_dashboard(filter.item_filter, warehouse_codes)

    # Save the dashboard to CSV
    save_dashboard(dashboard)

    print("Inventory dashboard generated successfully!")


if __name__ == "__main__":
    main()
