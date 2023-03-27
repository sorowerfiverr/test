import json
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import openpyxl
headers = {
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

# url = 'https://www.kuantokusta.pt/c/1568/trelas-e-coleiras/'
url = input('Enter Category URL(ex.https://www.kuantokusta.pt/c/1568/trelas-e-coleiras): ')
if url[-1] == '/':
    cat_id = url.split('/')[-3]
    cat_name = url.split('/')[-2].replace('-','_')

else:
    cat_id = url.split('/')[-2]
    cat_name = url.split('/')[-1].replace('-','_')


product_urls = []
for i in range(1,500):
    print(f'Searching Products From Page: {i}')
    new_url = f'https://api.kuantokusta.pt/products?pag={i}&category_id={cat_id}'
    r = requests.get(new_url,headers = headers)
    soup = bs(r.text,'html.parser')

    data = json.loads(str(soup)).get('productsGroup').get('products')
    if len(data)==0:
        break
    if len(data)!=0:
        for dat in data:
            url = 'https://www.kuantokusta.pt' + str(dat.get('productUrl'))
            if url not in product_urls:
                if 'http' not in str(dat.get('productUrl')):
                    product_urls.append(url)


print(f'Total Products Found: {len(product_urls)}')


datan = {}
listan = []

for prod_url in product_urls:
    print(f'Scraping Product URL: {prod_url}')

    proxy = {'http': 'http://brd-customer-hl_800a0fbb-zone-zone6:z5ydnrex081q@zproxy.lum-superproxy.io:22225',
            'https': 'http://brd-customer-hl_800a0fbb-zone-zone6:z5ydnrex081q@zproxy.lum-superproxy.io:22225'}
    for i in range(20):  
        try:      
            r = requests.get(prod_url,proxies = proxy,headers = headers)
            soup = bs(r.text,'html.parser')
        except:
            soup = ''
        # sleep(0.5)
    #     print(soup)
        try:
            ean = soup.find('span',attrs = {'class':'c-ijYvwD'}).text.strip()
            try:
                prod_name = soup.find('h1').text.strip()
            except:
                prod_name = ''
            try:
                prod_price = soup.find('span',attrs = {'data-test-id': 'topbox-offer-price'}).text.strip()
            except:
                prod_price = ''
            break
        except:
            ean  = ''
            prod_name = ''
            prod_price = ''

    print(f'EAN: {ean}')
    print(f'Product Name: {prod_name}')
    print(f'Product Price: {prod_price}')
    datan = {
        'Product URL': prod_url,
        'Product Name': prod_name,
        'Product Price': prod_price,
        'EAN': ean
    }
    listan.append(datan)
    df = pd.DataFrame(listan).to_excel(f'{cat_name}_category_output.xlsx',index = False)
df = pd.DataFrame(listan).to_excel(f'{cat_name}_category_output.xlsx',index = False)
