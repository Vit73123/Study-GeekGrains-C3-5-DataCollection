from lxml import etree

if __name__ == '__main__':
    # Парсинг HTML-документа
    tree = etree.parse("src/web_page.html")

    # Работа с xpath()
    print("Работа с xpath():")
    print("-----------------")
    print()

    title_element = tree.xpath("//title")
    print(title_element[0].text)

    title_element = tree.xpath("//title/text()")[0]
    print(title_element)

    title_element = tree.xpath("//p/text()")[0]
    print(title_element)

    list_items = tree.xpath("//li")

    print()
    for li in list_items:
        print(etree.tostring(li))
    print()
    for li in list_items:
        text = li.xpath("//text()")
        print(text)
    print()
    for li in list_items:
        text = li.xpath(".//text()")
        print(text)

    print()
    for li in list_items:
        text = map(str.strip, li.xpath(".//text()"))
        print(list(text))

    print()
    for li in list_items:
        text = ''.join(map(str.strip, li.xpath(".//text()")))
        print(text)

    # Работа с осями
    print()
    print("Работа с осями:")
    print("---------------")
    print()

    list_items = tree.xpath("//ul/descendant::li")
    for li in list_items:
        text = ''.join(map(str.strip, li.xpath(".//text()")))
        print(text)

    list_items = tree.xpath("///li/parent::*")
    for li in list_items:
        text = ''.join(map(str.strip, li.xpath(".//text()")))
        print(text)