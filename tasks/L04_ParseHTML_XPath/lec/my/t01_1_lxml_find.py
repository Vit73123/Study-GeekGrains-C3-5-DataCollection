from lxml import etree

def print_tree(element, depth=0):
    """Рекурсивная печать древовидной структуры элемента HTML"""

    # Вывод текущего элемента с соответствующим отступом
    print("-" * depth + element.tag)

    # Рекурсивная печать дочерних элементов с увеличенным отступом
    for child in element.iterchildren():
        print_tree(child, depth + 1)

if __name__ == '__main__':
    # Парсинг HTML-документа
    tree = etree.parse("src/web_page.html")
    print(tree)

    # Получение корневого элемента дерева
    root = tree.getroot()
    
    # Вывод структуры дерева
    print_tree(root)

    title_element = tree.find("head/title")
    print(title_element)
    print(title_element.text)

    p_element = tree.find("body/p")
    print(p_element.text)

    list_items = tree.findall("body/ul/li")
    print(list_items)
    for li in list_items:
        a = li.find("a")
        if a is not None:
            print(f"{li.text.strip()} {a.text}")
        else:
            print(li.text)

