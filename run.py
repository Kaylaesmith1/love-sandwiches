import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# CHECKED TO ENSURE API WAS WORKING
# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

def get_sales_data():

    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
    # Data ANY USER ENTERS will be a string -- need to change it to integer if it's a number
        print("Enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Eg: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        # USED TO MAKE SURE FUNCTION WORKS
        # print(f"The data provided is {data_str}")

        sales_data = data_str.split(',')
        # print(sales_data)
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        #CONVERTS string of numbers into integers. If statement checks if exactly 6 values are listed
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Six values are required; you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data error: {e}, please enter in a new value\n')
        return False

    return True   

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print('Updating sales worksheet.\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated successfully.\n')

    
data = get_sales_data() 
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)



# get_sales_data()