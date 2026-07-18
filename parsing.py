import requests
from bs4 import BeautifulSoup



def parsing(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0'}
    products = []
    while True:
        response = requests.get(url, headers=headers)

        catalog_soup = BeautifulSoup(response.text, "lxml")

        collect_links = catalog_soup.find_all('a', class_='card-head-url')
        links = []
        for link in collect_links:
           href = link.get('href')
           if href:
               links.append(href)

        for link in links:
            response = requests.get(link, headers=headers)
            response.raise_for_status()

            product_soup = BeautifulSoup(response.text, "lxml")

            # title
            title = product_soup.find('h2', class_='title').text

            # price
            currency = product_soup.find('span', class_='currency').text
            p = product_soup.find('span', class_='amount').text
            price = f"{currency} {p}"

            products.append({
                'title': title if title else "Not found",
                'price': price if price else "Not found",
            })
        next_b = catalog_soup.find('a', class_='page-link next')
        if next_b:
            url = next_b.get('href')
        else:
            break
    return products
