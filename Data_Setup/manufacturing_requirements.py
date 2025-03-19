from random import choices, choice, randint
import pandas as pd

from init import item_codes, number_of_items
from Data_Setup.shared_func import generate_code


def generate_manufacturing_requirements(num_items=None, output_path='./Datasets/Manufacturing_Requirements.csv'):
    """
    Generate manufacturing requirements data and save it to a CSV file.

    Parameters:
    -----------
    num_items : int, optional
        Number of items to consider for manufacturing. If None, uses the value from init.
    output_path : str, optional
        Path where the CSV file will be saved.

    Returns:
    --------
    pandas.DataFrame
        The generated manufacturing requirements data.
    """
    # Use the value from init if not specified
    if num_items is None:
        num_items = number_of_items

    number_of_manufacturing_goods = num_items
    manufacturing_goods = item_codes[: number_of_manufacturing_goods + number_of_manufacturing_goods % 2]

    inputs = choices(manufacturing_goods, k=number_of_manufacturing_goods // 2 + 1)

    manu_requirements = []
    manu_req_code_number = 1

    for manu_input in inputs:
        manu_req_code, manu_req_code_number = generate_code('MR', 3, manu_req_code_number)

        remainder = manufacturing_goods.copy()
        remainder.remove(manu_input)  # only prevents an item manufacturing itself
        output = choice(remainder)

        manufacturing_ratio = randint(6, 10) * 0.1
        input_weight = randint(1, 10) * 10
        output_weight = int(input_weight * manufacturing_ratio)

        manu_requirements.append([
            manu_req_code,
            manu_input,
            input_weight,
            output,
            output_weight
        ])

    df = pd.DataFrame(manu_requirements, columns=[
        "Manufacturing_Code",
        "Input_Code",
        "Input_Weight",
        "Output_Code",
        "Output_Weight"
    ])

    # Save to CSV
    df.to_csv(output_path, index=False)

    return df


# This allows other modules to import the DataFrame directly
manufacturing_requirements = generate_manufacturing_requirements()

if __name__ == "__main__":
    # When run directly, print the generated data
    test = pd.read_csv('./Datasets/Manufacturing_Requirements.csv')
    print(test)
