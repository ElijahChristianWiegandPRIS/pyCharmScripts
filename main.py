# This is a sample Python script.
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pandas as pd


def convert_excel_to_csv():
    excel_file = 'validationRulesOnly.xlsx'
    try:
        # read excel file
        df = pd.read_excel(excel_file)
        csv_fileName = excel_file.replace('.xlsx', '.csv')
        df.to_csv(csv_fileName, index=False)
        print(f"Excel file converted to CSV: {csv_fileName}")
        print(f"CSV file contains {len(df)} rows and {len(df.columns)} columns")
        return csv_fileName

    except Exception as e:
        print(f"Error reading Excel file: {e}")


def findCommonValidationRules():
    csv_file = 'validationRulesOnly.csv'

    # Check if CSV file exists, if not try to convert from Excel
    if not os.path.exists(csv_file):
        print(f"CSV file {csv_file} not found. Attempting to convert from Excel...")
        converted_file = convert_excel_to_csv()
        if converted_file is None:
            print(
                "Failed to convert Excel to CSV. Please ensure 'validationRulesOnly.xlsx' exists in the current directory.")
            return

    try:
        # Load the CSV file - both using comma separator (default)
        main_df = pd.read_csv(csv_file)  # Removed sep='|' - your file is comma-separated!

        # Display first few rows to understand the structure
        print("First 5 rows of the dataframe:")
        print(main_df.head())
        print("\nDataframe shape:", main_df.shape)
        print("\nColumn names:")
        print(main_df.columns.tolist())

        # Define state columns based on your actual data
        state_columns = ['TX', 'OK', 'PA', 'WI', 'OHM', 'OH-FR', 'AZ', 'MO', 'WV', 'TN', 'IA',
                         'KS-M', 'KS-B', 'TX-M', 'AR', 'IN-M', 'IN-MD', 'IL-M', 'IL-MD']

        # Check which state columns actually exist in your data
        available_state_columns = [col for col in state_columns if col in main_df.columns]
        print(f"\nAvailable state columns: {available_state_columns}")

        if not available_state_columns:
            print("No state columns found! Please check your column names.")
            return

        # Filter for rows where ALL available state values == "YES"
        print("\nFiltering for rules common to all states...")
        common_rules_df = main_df[main_df[available_state_columns].apply(lambda row: all(row == "YES"), axis=1)]

        print(f"\nFound {len(common_rules_df)} rules that are 'YES' for all states")

        # Check if 'Rule to Enact' column exists
        if 'Rule to Enact' in main_df.columns:
            print("\nSample of common rules:")
            print(common_rules_df[['Rule to Enact', 'Error or Warning', 'Rule Type']].head())

            # Save the common rules to a new CSV file
            output_file = "Common_Validation_Rules.csv"
            common_rules_df.to_csv(output_file, index=False)
            print(f"\nCommon rules saved to: {output_file}")
        else:
            print("'Rule to Enact' column not found in the data")
            print("Available columns:", main_df.columns.tolist())

    except Exception as e:
        print(f"Error processing CSV file: {e}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    convert_excel_to_csv()
    findCommonValidationRules()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
