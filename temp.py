import requests
from bs4 import BeautifulSoup





r = requests.get('https://www.gov.kz/memleket/entities/qriim/about/structure?lang=ru')
html = r.text
soup = BeautifulSoup(html, 'html.parser')

elements = soup.find_all('div', attrs={'class':'col-md-6'})
elements = [e for e in elements]


temp = []
for e in elements:
    if e.find('img') is None and not 'Руководство' in str(e):
        temp.append(e)
        print(e.find_all('div')[8].getText())


# print(elements)
print(len(temp))