import httpx
import wikipediaapi
from lxml import etree as ET

response = httpx.get('https://en.wikipedia.org/wiki/Stray_Kids')
with open('rre.html', 'w') as the_file:
    the_file.write(response.text)
tree = ET.parse('rre.html', ET.HTMLParser())
for element in tree.xpath('//a'):
    if 'href' in element.attrib.keys():
        href = element.attrib['href']
        if 'https' in href:
            print(href)