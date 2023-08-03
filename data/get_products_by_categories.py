import requests
import json
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_products_by_category(html):
    products_by_cat = dict()
    soup = BeautifulSoup(html, "html.parser")

    for span_id in range(6, 22):
        span_tag = soup.find("span", id=f"i-{span_id}")
        span_text = span_tag.next_element
        products_by_cat[span_text] = []

        table = span_tag.find_next("table")
        for row in table.find_all("tr")[1:]:
            product = row.find_all("td")[0].next_element
            products_by_cat[span_text].append(product)

    return products_by_cat


if __name__ == "__main__":
    html = get_html("https://pohudet.guru/tables/tablitsa-kalorijnosti-produktov/")

    if html:
        result = get_products_by_category(html)
        with open("products_by_categories_draft.py", "w", encoding="utf8") as f:
            f.write("products = ")
            json.dump(result, f, ensure_ascii=False)
