import re
from bs4 import BeautifulSoup as BS
import requests

headers = {
    "Accept": '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15'
}
url = 'https://www.gismeteo.ru'
req = requests.get(url, headers=headers)
src = req.text
soup = BS(src, 'lxml')
temp = soup.find(class_='unit unit_temperature_c')
print('Температура сейчас:',temp.text)
print(temp)
temp_time_forecast = soup.find(class_="widget-row widget-row-time").find_all('span')
time = []
k = ''
for temp_sec in temp_time_forecast:
    x = round(int(temp_sec.text) / 100)
    time.append(x)
for c in time:
    k += str(c)
    k += '   '
print('Время:       ',k)
cels = []
k = ''
values = soup.find(class_='values').find_all(class_='unit unit_temperature_c')
for temp_cels in values:
    cels.append(temp_cels.text)
for items in cels:
    k += str(items)
    k += ' '
print('Температура: ',k)