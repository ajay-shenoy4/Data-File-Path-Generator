import itertools
import pandas as pd

def main():
    # Define the dictionary with keys and initial values
    variables = {
        'parameter': None,
        'roi': None,
        'image_type': None,
    }

    # Ask how many conditions the user wants
    num_conditions = int(input("Enter the number of conditions: "))

    # Create a list to store condition keys
    conditions_list = ['condition'+str(i) for i in range(num_conditions)]

    # Add condition keys to the variables dictionary with initial values as None
    for condition in conditions_list:
        variables[condition] = None

    # Loop through the dictionary keys and ask for user input
    for key in variables:
        # Ask user for input
        user_input = input(f"Enter value(s) for {key} (comma-separated): ")
        # Split the input by commas and strip whitespace from each item
        values = [value.strip() for value in user_input.split(',')]
        # Store the list of values as the value for the key
        variables[key] = values

    # Ask user for the file path template
    base_path_template = input("Enter the file path template: ")

    # Ask user for column names to add from the dataframe
    columns_to_add = input("Enter column name(s) from the dataframe to add (comma-separated): ").split(',')

    # Print the updated dictionary
    print(variables)

    # Generate all possible combinations of values for the variables
    combinations = list(itertools.product(*variables.values()))

    dataframe_list = []
    # Iterate over each combination and format the template with the combination values
    for i, combination in enumerate(combinations):
        # Create a dictionary with variable names and their corresponding values
        values_dict = dict(zip(variables.keys(), combination))
        
        # Initialize dictionary to store data for DataFrame
        data = {key: [] for key in variables}

        # Append conditions to the base path template
        file_path = base_path_template.format(**values_dict)
        for j in range(num_conditions):
            file_path += f"_{values_dict[conditions_list[j]]}"
        
        # Add ".csv" to the end of the file path
        file_path += ".csv"

        print(f"Processing file path {i+1}: {file_path}")

        df = pd.read_csv(file_path)
      
        sample_number = len(df['filename'])

        for key, value in zip(data, combination):
            data[key] = sample_number * [value]

        # Add specified columns from the dataframe to the data dictionary
        for column in columns_to_add:
            data[column] = df[column]

        # Convert Series objects to lists
        data['filename'] = df['filename'].str.extract(r'(brain\d+)')[0].tolist()  # Extracts 'brain' followed by a number
        data['original_firstorder_Mean'] = df['original_firstorder_Mean'].tolist()

        dataframe_list.append(data)

    # Normalize the list of dictionaries into a list of dictionaries with single values
    normalized_data = [{k: v[i] for k, v in d.items()} for d in dataframe_list for i in range(len(list(d.values())[0]))]

    # Ask user for the file path to save the dataframe
    file_path_to_save = input("Enter the file path to save the dataframe: ")

    # Save the dataframe
    pd.DataFrame(normalized_data).to_csv(file_path_to_save, index=False)

    print(f"Dataframe saved as {file_path_to_save}")

    pd.DataFrame(normalized_data)

if __name__ == "__main__":
    main()


