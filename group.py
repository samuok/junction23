import pandas as pd
import numpy as np

import look_distance as lk
import utils

def elementwise_difference(vector1, vector2):
    return np.array(vector1) - np.array(vector2)

def calculate_elementwise_average(group, path, start, end):
    # Initialize a list to store the sum of elements for each position
    sum_elements = None
    count = 0

    # Iterate through the specified range of rows in the group
    for _, row in group.iloc[start:end].iterrows():
        # Access the elements based on the provided path
        elements = row
        for p in path:
            elements = elements[p]

        # Initialize sum_elements with the structure of the first element
        if sum_elements is None:
            sum_elements = [0] * len(elements)

        # Add up the elements element-wise
        sum_elements = [sum_val + el for sum_val, el in zip(sum_elements, elements)]
        count += 1

    # Calculate the element-wise average
    if count > 0:
        avg_elements = [sum_val / count for sum_val in sum_elements]
    else:
        avg_elements = []

    return avg_elements

def calculate_avg_difference(group, path, start, end):
    differences = []
    for i in range(len(group)-1):  # Iterate through the group with a step of 1
        # Access the current and next row in the group
        first_row = group.iloc[i]
        second_row = group.iloc[i+1]

        # Extract values based on the provided path
        first = first_row
        second = second_row
        for p in path:
            first = first[p]
            second = second[p]
        # Calculate the element-wise difference
        value = elementwise_difference(first[start:end], second[start:end])
        differences.extend(value)

    # Calculate the average difference for each element
    if differences:
        avg_differences = np.mean(differences)
    else:
        avg_differences = None

    return avg_differences

def count_non_nan(grouped_df, column_name):
    # Count non-NaN values for each group in the specified column
    count_non_nan_values = grouped_df[column_name].agg(lambda x: x.notna().sum())

    return count_non_nan_values


def build_group(filename, typ):
    filepath = utils.get_path(filename)
    df = utils.get_dataframe(filepath)
    # Create a new column 'group_id' for grouping every 5 rows
    df['group_id'] = df.index // 60

    # Apply the custom function to each group
    avg_differences_right_movement = df.groupby('group_id').apply(lambda x: calculate_avg_difference(x, ["afe", 0, "m", 0],0, 5))
    avg_differences_left_movement = df.groupby('group_id').apply(lambda x: calculate_avg_difference(x, ["afe", 1, "m", 0], 0, 5))

    avg_left= df.groupby('group_id').apply(lambda x: calculate_elementwise_average(x, ["afe", 1, "m", 0], 0, 5))
    #avg_left= avg_left.apply(lambda x: eye.get_dir_strings(x,x)[0])
    avg_right = df.groupby('group_id').apply(lambda x: calculate_elementwise_average(x, ["afe", 0, "m", 0], 0, 5))
    #avg_right = avg_right.apply(lambda x: eye.get_dir_strings(x, x)[1])


    # Apply get_look_distance to each pair of rows from avg_left and avg_right
    look = pd.Series([lk.get_look_distance(l, r) for l, r in zip(avg_left, avg_right)])

    # If you want the result as a DataFrame
    #look = look.to_frame(name='look_distance')
    #blinks
    blinks = df.groupby('group_id').apply(lambda x: count_non_nan(x, "blinks"))
    # Combine the results
    combined_df = pd.concat([avg_differences_left_movement.reset_index(name='left_erratic'),
                             avg_differences_right_movement.reset_index(name='right_erratic'),
                             avg_left.reset_index(name='left'),
                             avg_right.reset_index(name='right'),
                             blinks.reset_index(name='blink_count'),
                             look.reset_index(name="distance")], axis=1)

    # Drop duplicate 'group_id' columns if necessary
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    # Add a new column with the value from 'typ'
    combined_df['type'] = typ

    return combined_df

def combine_dataframes(df1, df2):
    # Concatenate the two dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)

    return combined_df

def process_and_combine_files(file_paths, typ):
    combined_df = None

    for file in file_paths:
        df = build_group(file, typ)

        if combined_df is None:
            combined_df = df
        else:
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df