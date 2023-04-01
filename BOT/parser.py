import requests
from bs4 import BeautifulSoup

url = 'https://ligovka.ru/'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'lxml')
name = bs.find_all('th',)

value = bs.find_all('td', 'money_price')
dict = {}
def create_dict():
    dict[f'{name[1].text}/RU'] = value[0].text
    dict[f'{name[3].text}/RU'] = value[2].text
    dict[name[5].text] = value[4].text
    dict[f'{name[1].text}/{name[3].text}'] = value[5].text
    dict[f'RU/{name[1].text}'] = round(1 / float(value[1].text), 4)
    dict[f'RU/{name[3].text}'] = round(1 / float(value[3].text), 4)
    return dict

create_dict()
if __name__ == '__main__':
    print(create_dict())
