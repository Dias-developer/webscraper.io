# importing
from parser import parsing

url = 'https://webscraper.io/test-sites/pagination'

parsed = parsing(url)

print(len(parsed))
print(parsed)



