import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided
#     """
#     print('Updating sales worksheet.\n')
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print('Sales worksheet updated successfully.\n')

# def update_surplus_worksheet(new_surplus_data):
#     """
#     Update surplus worksheet, add new row with the list data provided
#     """
#     print('Updating surplus worksheet.\n')
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(new_surplus_data)
#     print('You did it! Surplus worksheet updated successfully.\n')

# Refactored into one function from above two functions
def update_worksheet(data, worksheet):
    """
    Update worksheet
    """
    print(f'Updating worksheet: {worksheet}. \n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'Worksheet: {worksheet} updated successfully. \n')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print('Calculating surplus data. \n')
    stock = SHEET.worksheet('stock').get_all_values()
    # SLICE OUT LAST ROW USING -1 IN SQUARE BRACKETS
    stock_row = stock[-1]
    # PRINTS STOCK AND SALES ROWS SO WE CAN SEE VALUES
    # print(f'stock row: {stock_row}')
    # print(f'sales row: {sales_row}')
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        # convert the stock variable into an integer
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def last_five_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet('sales')
    # get a list of numbers for just column 3 of sales
    # column = sales.col_values(3)
    # print(column)

    # get all lists using a for loop
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def main(): 
    """
    Run all program functions
    """
    data = get_sales_data() 
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    print(new_surplus_data)


print('Welcome to Love Sandwiches Data Automation')
# call out main() to test other functions
# main()
sales_columns = last_five_sales()



# get_sales_data()