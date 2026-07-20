import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor # Для многопоточности
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry # Для того что бы парсер не падал
import threading

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0'}

def make_session(): # Для создания сессий для каталога
    session = requests.Session()
    session.headers.update(headers)

    retry = Retry(
    total=5,
    backoff_factor=1,                 # 1s, 2s, 4s, 8s...
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    respect_retry_after_header=True,
    )

    session.mount('https://', HTTPAdapter(max_retries=retry))
    session.mount('http://', HTTPAdapter(max_retries=retry))

    return session

thread_local = threading.local()
def get_session(): # Для создания сессий для товаров
    if not hasattr(thread_local, 'session'):
        thread_local.session = make_session()
    return thread_local.session


def parse_product(link): # Парсит товары
    try:
        session = get_session()
        response = session.get(link, timeout=10)
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



def parsing(url): # Парсит каталог с пагинацией
    products = []
    session = make_session()
    with ThreadPoolExecutor(max_workers=10) as executor:

        while True:
            response = session.get(url, timeout=10)
            response.raise_for_status()

            catalog_soup = BeautifulSoup(response.text, "lxml")

            collect_links = catalog_soup.find_all('a', class_='card-head-url')
            links = [link.get('href') for link in collect_links if link.get('href')]

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
