from Data_Setup.available_stock import generate_stock_table
from Data_Setup.inbound import generate_inbound_data
from Data_Setup.internal_transfer import generate_internal_transfers
from Data_Setup.manufacturing_requirements import generate_manufacturing_requirements
from Data_Setup.manufacturing_plan import generate_manufacturing_plan
from Data_Setup.outbound import generate_outbound_data


def main():
    # Generate manufacturing requirements first (if needed)
    req_df = generate_manufacturing_requirements()
    print("Manufacturing requirements generated successfully!")

    # Generate manufacturing plan using those requirements
    manufacturing_df = generate_manufacturing_plan()
    print("Manufacturing plan generated successfully!")

    # Generate other datasets
    stock_df = generate_stock_table()
    print("Stock table generated successfully!")

    inbound_df = generate_inbound_data()
    print("Inbound data generated successfully!")

    transfers_df = generate_internal_transfers()
    print("Internal transfers generated successfully!")

    outbound_df = generate_outbound_data()
    print("Outbound data generated successfully!")

    print("All datasets generated successfully!")


if __name__ == "__main__":
    main()
