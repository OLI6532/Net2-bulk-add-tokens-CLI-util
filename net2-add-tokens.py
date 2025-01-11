import csv
import os.path
from datetime import datetime

def main():
    print("""\033[1mNet2 Bulk Add Tokens Import Utility:\033[0m
    
This CLI Utility processes a CSV file containing new token numbers and generates
a file which can be used to import the new tokens into a Net2 database
""")

    file_path = input("Path to CSV file containing new token numbers: ").strip()

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        # Attempt to open the user-provided file
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            columns = reader.fieldnames

            print(f'File loaded. Found {len(rows)} records and the following headers:')
            print(", ".join(columns))
    except Exception as e:
        print(f'Error reading the CSV file: {e}')
        return
    print("")

    try:
        # Identify the token number column
        if 'Token number' not in columns: # 'Token number' is the default header produced by a Net2 custom report
            # If 'Token number' cannot be found, ask the user to provide the correct column index.
            for i, col in enumerate(columns, start=1):
                print(f'{i} – {col}')
            selected_index = int(input("Enter number of the token column: "))
            token_column = columns[selected_index - 1]
        else:
            token_column = 'Token number'

        # The name to give the new users
        first_name = input("Required: Name to use for the new users: ").strip()
        if first_name == "":
            print('Error: A name must be provided for the new users.')
            return

        # The ID to begin the first user at
        start_id = int(input(
            "\nEnter the starting ID for new users.\nWARNING: Any users with a duplicate ID will be overwritten. Leave blank for 900000: ").strip() or 0)
        if start_id == 0:
            start_id = 900000

        # What access level to assign to the new users
        access_level = input("Enter the Access Level for new users (leave blank for 'Working hours'): ").strip()
        if access_level == "": access_level = "Working hours"

        # What department to put the new users in
        department = input("Department for the new users (leave blank for none): ").strip()
        if department == "":
            department = "(none)"

    except Exception as e:
        print(f"Error collecting inputs: {e}")
        return

    output_rows = []
    for i, row in enumerate(rows):
        output_row = {
            'Surname': f'{i + 1}',
            'First Name': first_name,
            'Middle Name': '',
            'Card Number': f"1#{row[token_column]}",
            'PIN': '',
            'Department': department,
            'Access level': access_level,
            'Telephone': '',
            'Extension': '',
            'Fax': '',
            'Activation Date': datetime.now().strftime("%d/%m/%Y"),
            'Expiration date': '',
            'Address 1': '',
            'Address 2': '',
            'Town': '',
            'County': '',
            'Post code': '',
            'Home telephone': '',
            'Home fax': '',
            'Mobile': '',
            'Email': '',
            'Position': '',
            'Start date': '',
            'Car registration': '',
            'Notes': '',
            'Personnel number': '',
            'User ID': start_id + i,
        }
        output_rows.append(output_row)

    try:
        output_file_path = file_path.replace('.csv', '_parsed.csv')
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output_rows[0].keys())
            writer.writeheader()
            writer.writerows(output_rows)
            print(f"Output file saved successfully at '{output_file_path}'.")
    except Exception as e:
        print(f"Error writing the output file: {e}")
        return

    print("Processing complete. Exiting program.")


if __name__ == '__main__':
    main()
