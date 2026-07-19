import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0'}

def parse_product(link):
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # title
        title = soup.find('h2', class_='title')

        # price
        currency = soup.find('span', class_='currency').get_text(strip=True)
        p = soup.find('span', class_='amount').get_text(strip=True)
        price = f"{currency} {p}"

        return {
            'title': title.get_text(strip=True) if title else 'Not found',
            'price': price if price else 'Not found',
        }
    except Exception as e:
        print(f"Ошибка {link}: {e}")
        return None

def parsing(url):
    products = []
    session = requests.Session()
    session.headers.update(headers)
    while True:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        catalog_soup = BeautifulSoup(response.text, "lxml")

        collect_links = catalog_soup.find_all('a', class_='card-head-url')
        links = []
        for link in collect_links:
           href = link.get('href')
           if href:
               links.append(href)

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(parse_product, links)

            for product in results:
                if product:
                    products.append(product)

        next_b = catalog_soup.find('a', class_='page-link next')
        if next_b:
            url = next_b.get('href')
        else:
            break

    return products
