from lxml import etree

if __name__ == '__main__':
    # Парсинг HTML-документа
    tree = etree.parse("src/web_page.html")
    html = tree.getroot()

    # Работа с cssselect()
    print("Работа с cssselect():")
    print("---------------------")
    print()

    title_element = html.cssselect("title")
    print(title_element[0].text)

    print()
    title_element = html.cssselect("p")
    print(title_element[0].text)

    print()
    list_items = html.cssselect("li")
    for li in list_items:
        a = li.cssselect("a")
        if len(a) == 0:
            print(li.text)
        else:
            print(f"{li.text.strip()} {a[0].text}")