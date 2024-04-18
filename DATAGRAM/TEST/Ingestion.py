import json
import pymysql


connection = pymysql.connect(
    host='localhost',
    user='louay',
    password='louay',
    database='test'
)

cursor = connection.cursor()

with open('product_data.json', 'r') as file:
    product_data = json.load(file)

for product in product_data:
    insert = '''
    INSERT INTO products (Name, Brand, Price, Product_url, Image_url)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert, (
        product['name'],
        product['brand'],
        product['price'],
        product['product_url'],
        product['image_url']
    ))


connection.commit()
connection.close()


