import gspread as gr
import requests
import psycopg2
from psycopg2 import Error
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
rate_USD = soup.find('div', class_='col-md-2 col-xs-9 _right mono-num').getText(strip=True)
current_rate = rate_USD[:7]
current_rate = float(current_rate.replace(',', '.'))

# Convert USD/RUB
values_col5 = []
for price in values_col3[1:]:
    price = float(price) * current_rate
    values_col5.append(price)

# Changing the type of date
correct_date = []
for date in values_col4:
    date = date.replace('.', '/')
    correct_date.append(date)

# Connect to DB
try:
    conn = psycopg2.connect(dbname='job_test', user='postgres',
                            password='qwerty', port='5432',
                            host='localhost')

    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS test')

    # Create DB
    create_table = '''CREATE TABLE "test"
    ("№" INTEGER,
    "заказ №" INTEGER,
    "стоимость,$" INTEGER,
    "срок поставки" TEXT,
    "стоимость в руб." INTEGER);'''

    cursor.execute(create_table)
    conn.commit()

    # Add values in DB
    # for v1 in values_col1[1:]:
    #     for v2 in values_col2[1:]:
    #         for v3 in values_col3[1:]:
    #             for v4 in correct_date[1:]:
    #                 for v5 in values_col5:
    #                     cursor.execute(f'INSERT INTO test VALUES ({v1}, {v2}, {v3}, {v4}, {v5})')
    # for v1 in values_col1[1:]:
    #     cursor.execute(f'INSERT INTO test ("№") VALUES ({v1})')
    #     for v2 in values_col2[1:]:
    #         cursor.execute(f'INSERT INTO test ("заказ №") VALUES ({v2})')
    #         for v3 in values_col3[1:]:
    #             cursor.execute(f'INSERT INTO test ("стоимость,$") VALUES ({v3})')
    #             for v4 in correct_date[1:]:
    #                 cursor.execute(f'INSERT INTO test ("срок поставки") VALUES ({v4})')
    #                 for v5 in values_col5:
    #                     cursor.execute(f'INSERT INTO test ("стоимость в руб.") VALUES ({v5})')

    conn.commit()

    table = cursor.execute('SELECT * FROM test')
    print(table)

except (Exception, Error) as error:
    print("Error with PostgreSQL:", error)
finally:
    if conn:
        conn.commit()
        cursor.close()
        conn.close()

