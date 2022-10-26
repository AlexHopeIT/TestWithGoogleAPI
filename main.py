import gspread as gr
import requests
from bs4 import BeautifulSoup

# Connect to Google API
sheets_id = '14DJ3GP4oPVDyJgpg0PhWXA61qp_Cc67qX5QmRfB2t8c'

gc = gr.service_account(filename='keys.json')
sht1 = gc.open_by_key(sheets_id)
worksheet = sht1.sheet1

# Get values of columns at Sheet
values_col1 = worksheet.col_values(1)
values_col2 = worksheet.col_values(2)
values_col3 = worksheet.col_values(3)
values_col4 = worksheet.col_values(4)

# Create parser
url_cb = 'https://www.cbr.ru/'
my_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}
responce = requests.get(url_cb, headers=my_headers)
soup = BeautifulSoup(responce.content, 'html.parser')
course_USD = soup.find('div', class_='col-md-2 col-xs-9 _right mono-num').getText(strip=True)
current_course = course_USD[:7]
current_course = float(current_course.replace(',', '.'))

# Convert USD/RUB
values_col5 = []
for price in values_col3[1:]:
    price = float(price) * current_course
    values_col5.append(price)

print(values_col5)

