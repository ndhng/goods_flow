from random import choices, choice, randint

import pandas as pd

from Data_Setup.init import item_codes, number_of_items

number_of_manufacturing_goods = number_of_items
manufacturing_goods = item_codes[: number_of_manufacturing_goods + number_of_manufacturing_goods % 2]
# print(manufacturing_goods)

inputs = choices(manufacturing_goods, k=number_of_manufacturing_goods // 2 + 1)
# print(inputs)

manu_requirements = []
for input in inputs:
    remainder = manufacturing_goods.copy()
    remainder.remove(input) # only prevents an item manufacturing itself
    output = choice(remainder)

    manufacturing_ratio = randint(6, 10)*0.1
    input_weight = randint(1, 10)*10
    output_weight = int(input_weight * manufacturing_ratio)
    # print(f'To produce {output_weight}kg of {output}, requires {input_weight}kg of {input}')
    manu_requirements.append([input, input_weight, output, output_weight])

df = pd.DataFrame(manu_requirements, columns = ["Input_Code" ,"Input_Weight","Output_Code", "Output_Weight"]).to_csv('../Datasets/Manufacturing_Requirements.csv', index=False)

if __name__ == "__main__":
    test = pd.read_csv('../Datasets/Manufacturing_Requirements.csv')
    print(test)