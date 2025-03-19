import pandas as pd

def separate_manufacturing_plan(csv='Datasets/Manufacturing_Plan.csv'):

    manufacturing_plan = pd.read_csv(csv)

    separated = []
    element_name = 'Production Order'
    for index, row in manufacturing_plan.iterrows():
        production_order_number = row['Production_Order_Code']
        warehouse_code = row['Warehouse']

        input_code = row['Input']
        input_date = row['Input_Date']
        input_amount = row['Input_Weight']
        separated.append([element_name + ' (Input)', production_order_number + '-1', production_order_number, input_code, input_date, input_amount * -1, warehouse_code])

        output_code = row['Output']
        output_date = row['Output_Date']
        output_amount = row['Output_Weight']
        separated.append([element_name + ' (Output)', production_order_number + '-2', production_order_number, output_code, output_date, output_amount, warehouse_code])

    separated_df = pd.DataFrame(separated, columns=['Element_Name', 'Element_Code', 'Element_Number', 'Item_Code', 'Date', 'Amount', 'Warehouse_Code'])

    return separated_df

def separate_internal_transfer(csv='Datasets/Internal_Transfers.csv'):

    internal_transfers = pd.read_csv(csv)

    separated = []
    element_name = 'Internal Transfer'
    for index, row in internal_transfers.iterrows():
        internal_transfer_number = row['Element_Code']
        item_code = row['Item_Code']
        amount = row['Amount']

        origin_warehouse_code = row['Warehouse_Origin']
        origin_date = row['Date_Origin']
        separated.append([element_name + ' (Out)', internal_transfer_number + '-1', internal_transfer_number, item_code, origin_date, amount * -1, origin_warehouse_code])

        destination_warehouse_code = row['Warehouse_Destination']
        destination_date = row['Date_Arrival']
        separated.append([element_name + ' (In)', internal_transfer_number + '-2', internal_transfer_number, item_code, destination_date, amount, destination_warehouse_code])

    separated_df = pd.DataFrame(separated, columns=['Element_Name', 'Element_Code', 'Element_Number', 'Item_Code', 'Date', 'Amount', 'Warehouse_Code'])
    return separated_df


if __name__ == "__main__":
    manufacture = separate_manufacturing_plan()
    transfer = separate_internal_transfer()
