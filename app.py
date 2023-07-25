from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By

# kitap sepeti
driver = webdriver.Chrome()
driver.get('https://www.kitapsepeti.com/')
# Select Item
selected_input_search = driver.find_element(By.CSS_SELECTOR, "input#live-search")
selected_input_search.send_keys('python')

selected_input_search_button = driver.find_element(By.CSS_SELECTOR, "input#searchBtn")
selected_input_search_button.click()

driver.find_element(By.XPATH, "/html//div[@id='filtreStock']/div[@class='row stoktakiler']//label/span/i[1]").click()

# Get values and Edit values
kitap_sepeti_books = []
kitap_sepeti_update_books = []
strs_1 = [f"{x}" for x in range(1, 55)]
for i in strs_1:
    selected_books = driver.find_elements(By.XPATH,
                                          f"/html//div[@id='katalog']/div[@class='col col-12 p-left']/div/div/div[{i}]/div")
    for value in selected_books:
        kitap_sepeti_books.append(value.text)

for i in range(len(kitap_sepeti_books)):
    value = kitap_sepeti_books[i].split('\n')
    kitap_sepeti_update_books.append(value)

kitap_sepeti_books.clear()

kitap_sepeti_books_dict = {}

for i in range(len(kitap_sepeti_update_books)):
    kitap_sepeti_books_dict = {
        'title': kitap_sepeti_update_books[i][0],
        'publisher': kitap_sepeti_update_books[i][1],
        'writers': kitap_sepeti_update_books[i][2],
        'price': kitap_sepeti_update_books[i][3]

    }
    kitap_sepeti_books.append(kitap_sepeti_books_dict)
title = []
writers = []
publisher = []
price = []
key = list(kitap_sepeti_books[0].keys())
for value in kitap_sepeti_books:
    title.append(value.get('title'))
    writers.append(value.get('writers'))
    publisher.append(value.get('publisher'))
    price.append(value.get('price'))

# Create flask app
app = Flask(__name__)

stores = [
    {

        "name": 'my_store',
        "items": [
            {
                'value': kitap_sepeti_books
            }
        ]

    }
]


@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {'stores': stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'], 'items': []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {"name": request_data["name"], "value": request_data["value"]}
            store["items"].append(new_item)
            return new_item
    return {"message": "Store not found"}, 404

