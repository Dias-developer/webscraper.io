import requests
from bs4 import BeautifulSoup

def parsing(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0'}


    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    collect_links = soup.find_all('a', class_='card-head-url')
    links = []
    products = []
    for link in collect_links:
        href = link.get('href')
        if href:
            links.append(href)

    for link in links:
        response = requests.get(link, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # title
        title = soup.find('h2', class_='title').text

        # price
        currency = soup.find('span', class_='currency').text
        p = soup.find('span', class_='amount').text
        price = f"{currency} {p}"

        products.append({
            'title': title,
            'price': price,
        })
    return products
