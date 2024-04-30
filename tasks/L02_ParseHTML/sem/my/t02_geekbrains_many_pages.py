import requests
from bs4 import BeautifulSoup
from pprint import pprint

# from fake_useragent import UserAgent

# ua = UserAgent()

url = "https://gb.ru"

headers = {
    # "User-Agent": ua.random,
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    "Accept": "*/*",
}

params = {
    'page': 1,
}

session = requests.session()

all_posts = []

while True:
    response = session.get(url + "/posts", params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.findAll('div', {'class': 'post-item'})

    if not posts:
        break

    for post in posts:
        post_info = {}

        name_info = post.find('a', {'class': 'post-item__title'})
        post_info['name'] = name_info.getText()
        post_info['url'] = url + name_info.get('href')

        add_info = post.find('div', {'class': 'text-muted'}).findChildren('span')
        post_info['views'] = int(add_info[0].getText())
        post_info['comments'] = int(add_info[0].getText())

        all_posts.append(post_info)
    print(f"Обработано {params['page']} страница")
    params['page'] += 1

pprint(all_posts)
pprint(len(all_posts))
