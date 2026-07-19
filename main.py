# importing
from parsing import parsing
from save import save_excel
import time
# url
url = 'https://webscraper.io/test-sites/pagination'

# web scraping
start = time.time()
parsed = parsing(url)
end = time.time()
# save in Excel
save_excel(parsed)
print(f"Время выполнения: {end - start:.2f} секунд")