# importing
from parsing import parsing
from save import save_excel

# url
url = 'https://webscraper.io/test-sites/pagination'

# web scraping
parsed = parsing(url)

# save in Excel
save_excel(parsed)