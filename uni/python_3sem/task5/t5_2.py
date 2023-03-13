import httpx
import wikipediaapi
from lxml import etree as ET

response = httpx.get('https://en.wikipedia.org/wiki/Stray_Kids')
with open('rre.html', 'a') as the_file:
    the_file.write(response.text)
tree = ET.parse('rre.html')
print(tree)