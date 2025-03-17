from datetime import date

number_of_items = 15
number_of_warehouses = 4
start_date = date(2025,1,1)

item_codes = []
for i in range(1,number_of_items+1):
    zeros = "0"*(3-len(str(i)))
    item_codes.append("Item"+zeros+str(i))

warehouse_codes = []
for i in range(1,number_of_warehouses+1):
    zeros = "0"*(3-len(str(i)))
    warehouse_codes.append("WH"+zeros+str(i))

# Inbound table constants
number_of_inbounds = 100
inbound_frequency = 0.3 # the higher this number, the less frequently goods is bought in a day
combined_PO_frequency = 0.9 # the lower this number, the more items are combined in a SO
max_no_inbound_days = 3

# Outbound table constants
number_of_outbounds = 100
outbound_frequency = 0.3 # the higher this number, the less frequently goods is sold in a day
combined_SO_frequency = 0.9 # the lower this number, the more items are combined in a SO
max_no_outbound_days = 3

# Internal Transfers table constants
number_of_transfers = 20
internal_transfer_days = 10
transfer_frequency = 0.95
combined_IT_frequency = 0.9
max_no_IT_days = 10