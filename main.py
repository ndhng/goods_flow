import pandas as pd

from Data_Setup.available_stock import generate_stock_table
from Data_Setup.inbound import generate_inbound_data
from Data_Setup.internal_transfer import generate_internal_transfers
from Data_Setup.manufacturing_plan import generate_manufacturing_plan
from Data_Setup.outbound import generate_outbound_data

from init import start_date, warehouse_codes
import filter

from divide_input_output import separate_manufacturing_plan, separate_internal_transfer

# Generate all datasets
def generate_all_datasets():
    generate_manufacturing_plan(regenerate_requirements=True)
    generate_stock_table()
    generate_inbound_data()
    generate_internal_transfers()
    generate_outbound_data()

# generate_all_datasets() ##### Comment out to prevents making new datasets

# Read and filter starting stock
stock_df = pd.read_csv('./Datasets/Available_Stock.csv')
previous_date = filter.starting_date - pd.DateOffset(days=1)
previous_date = previous_date.strftime('%Y-%m-%d')
stock_df = stock_df[stock_df['Date'] == previous_date]
stock_df = stock_df[stock_df['Item_Code'] == filter.item_filter]

# Read inbound & outbound
outbound_df = pd.read_csv('./Datasets/Outbound.csv')
inbound_df = pd.read_csv('./Datasets/Inbound.csv')

# Transform manufacturing_df and transfers_df
manufacturing_df = separate_manufacturing_plan()
transfers_df = separate_internal_transfer()

# Filter all dfs for only item_code
inbound_df = inbound_df[inbound_df["Item_Code"] == filter.item_filter]
outbound_df = outbound_df[outbound_df["Item_Code"] == filter.item_filter]
manufacturing_df = manufacturing_df[manufacturing_df["Item_Code"] == filter.item_filter]
transfers_df = transfers_df[transfers_df["Item_Code"] == filter.item_filter]

# Initialize first row
first_row = [previous_date, 'Starting Stock', None, f'Item Code: {filter.item_filter}', None, None]
for warehouse in warehouse_codes:
    first_row.append(stock_df[stock_df['Warehouse_Code'] == warehouse]['Stock_Amount'].sum())

cols = ['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']
for warehouse in warehouse_codes:
    cols.append(warehouse)

dashboard = pd.DataFrame(columns=cols, index=[0])
dashboard.iloc[0] = first_row

# Prepare inbound dataframe for merging
inbound_copy = inbound_df.copy()
inbound_copy['Element_Name'] = 'Purchase Order Item'
inbound_copy = inbound_copy[['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']]

# Prepare outbound dataframe for merging
outbound_copy = outbound_df.copy()
outbound_copy['Element_Name'] = 'Sales Order Item'
outbound_copy['Amount'] = outbound_copy['Amount'] * -1
outbound_copy = outbound_copy[['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']]

# Manufacturing and transfers already have the correct Element_Name from separate functions
# Just ensure they have the right columns in the right order
manufacturing_copy = manufacturing_df[
    ['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']]
transfers_copy = transfers_df[['Date', 'Element_Code', 'Element_Number', 'Element_Name', 'Warehouse_Code', 'Amount']]

# Create empty columns for warehouses in all dataframes
for warehouse in warehouse_codes:
    inbound_copy[warehouse] = None
    outbound_copy[warehouse] = None
    manufacturing_copy[warehouse] = None
    transfers_copy[warehouse] = None

# Combine all dataframes
combined_df = pd.concat([inbound_copy, outbound_copy, manufacturing_copy, transfers_copy])

# Append the combined dataframe to the dashboard
dashboard = pd.concat([dashboard, combined_df], ignore_index=True)

# Sort the final dashboard by date
dashboard = dashboard.sort_values(by='Date', ignore_index=True)

# Process the dashboard to update warehouse balances
for index, row in dashboard.iterrows():
    if index == 0:
        continue
    else:
        prev = dashboard.loc[index - 1]
        for warehouse in warehouse_codes:
            if warehouse == row['Warehouse_Code']:
                dashboard.loc[index, warehouse] = dashboard.loc[index - 1, warehouse] + row['Amount']
            else:
                dashboard.loc[index, warehouse] = dashboard.loc[index - 1, warehouse]

dashboard.to_csv('./Dashboard.csv', index=False)


