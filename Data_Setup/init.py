from datetime import date

number_of_items = 15
number_of_warehouses = 4
start_date = date(2025,1,1)

item_codes = []
for i in range(1,number_of_items):
    zeros = "0"*(3-len(str(i)))
    item_codes.append("Item"+zeros+str(i))

warehouse_codes = []
for i in range(1,number_of_warehouses):
    zeros = "0"*(3-len(str(i)))
    warehouse_codes.append("WH"+zeros+str(i))

number_of_outbounds = 100
number_of_inbounds = 100

