import gspread

path_to_keys = gspread.service_account(
    filename='D:/Programs/pythonProject/Test for the Chanelservice/resources/keys.json')

test_sheet = path_to_keys.open('Test for the Chanelservice')


