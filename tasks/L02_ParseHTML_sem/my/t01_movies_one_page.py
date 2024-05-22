import requests
from bs4 import BeautifulSoup
import pprint

# from fake_useragent import UserAgent

# ua = UserAgent()
# print(ua.safari)
# print(ua.random)

# url = "https://www.boxofﬁcemojo.com/intl/?ref_=bo_nb_hm_tab"
url = "https://www.boxofficemojo.com"

headers = {
    # "User-Agent": ua.random,
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    "Accept": "*/*",
}

params = {
    "ref_": "bo_nb_hm_tab",
}

session = requests.session()

response = session.get(url + "/intl", params=params, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.findAll('tr')

films = []

for row in rows[2:]:
    film = {}

    try:
        # area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).find('a')
        area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0]
        film['area'] = [area_info.getText(), url + area_info.get('href')]

        weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
        film['weekend'] = [weekend_info.getText(), url + weekend_info.get('href')]

        film['releases'] = row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText()

        frelease_info = row.find('td', {'class': 'mojo-field-type-release'}).findChildren()[0]
        film['frelease'] = [frelease_info.getText(), url + frelease_info.get('href')]

        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText(), url + distributor_info.get('href')]

        films.append(film)
    except:
        continue

    print()

pprint. pprint(films)

# test_link = soup.find('a', {'class': 'a-link-normal'})
# print(test_link)
# print(response.status_code)
