import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_starting_url(starting_url):
    visited_urls = set()
    urls_to_crawl = [starting_url]
    crawled_links = set()  

    while urls_to_crawl:
        current_url = urls_to_crawl.pop(0)

        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }
            response = requests.get(current_url, headers=headers)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                absolute_url = urljoin(current_url, link['href'])
                if absolute_url.startswith(starting_url) and '#tm-search-mobile' not in absolute_url and '#tm-mobile' not in absolute_url:
                    urls_to_crawl.append(absolute_url)
                    crawled_links.add(absolute_url)  
        except Exception as e:
            print("Error crawling:", current_url)
            print(e)

    
    return crawled_links



def extract_products(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.get(url)


    driver.implicitly_wait(10)  
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []

    for product in soup.find_all('div', class_='uk-card'):
        name = product.find('h3', class_='product-name').text.strip()
        brand = product.find('div', class_='uk-width-expand uk-first-column').text.strip()
        price_div = product.find('div', class_='uk-grid uk-grid-small uk-prix-final uk-margin-remove-top uk-flex-center')

        price = price_div.find('span', class_='uk-price').text.strip().replace("\xa0€", "").replace(",", ".")
        price_float = float(price)
        rounded_price = round(price_float, 2)
        product_url = product.find('a', class_='product-item-link')['href']
        div_photo_product = soup.find('div', class_='uk-photo-product')


        img_tag = div_photo_product.find('img')


        image_url = img_tag['src']

        
        product_info = {
            'name': name,
            'brand': brand,
            'price': rounded_price,
            'product_url': product_url,
            'image_url': image_url
        }

        
        products.append(product_info)
    return products

if __name__ == "__main__":
    
    starting_url = "https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html"
    links = crawl_starting_url(starting_url)
    

    all_products = []  

    for link in links:
        product_info = extract_products(link)
        all_products.extend(product_info)  

    
    with open('products_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, indent=4, ensure_ascii=False)

        


