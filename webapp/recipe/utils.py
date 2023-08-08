import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import requests
from webapp.config import (
    YANDEX_TRANSLATE_API_KEY,
    YANDEX_FOLDER_ID,
    SPOONACULAR_API_KEY,
)


def get_translation(texts, source_language_code, target_language_code):
    body = {
        "targetLanguageCode": target_language_code,
        "sourceLanguageCode": source_language_code,
        "texts": texts,
        "folderId": YANDEX_FOLDER_ID,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key " + YANDEX_TRANSLATE_API_KEY,
    }

    try:
        result = requests.post(
            "https://translate.api.cloud.yandex.net/translate/v2/translate",
            json=body,
            headers=headers,
        )
        result.raise_for_status()
        return result.json()["translations"]
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


class SpoonacularAPI:
    base_url = "https://api.spoonacular.com/recipes/"
    api_key = SPOONACULAR_API_KEY
    headers = {
        "Content-Type": "application/json",
    }

    @classmethod
    def find_recipe(
        cls, recipe_name="", recipe_category="", recipe_cuisine="", recipe_diet=""
    ):
        if recipe_name != "":
            translate = get_translation(
                texts=[recipe_name],
                source_language_code="ru",
                target_language_code="en",
            )
            recipe_name = translate[0]["text"]
        url = cls.base_url + "complexSearch"
        querystring = {
            "apiKey": SPOONACULAR_API_KEY,
            "query": recipe_name,
            "type": recipe_category,
            "cuisine": recipe_cuisine,
            "diet": recipe_diet,
            "number": 30,
        }
        if all(
            [
                data == ""
                for data in [recipe_name, recipe_category, recipe_diet, recipe_cuisine]
            ]
        ):
            querystring.update({"number": 9})

        try:
            result = requests.get(url, headers=cls.headers, params=querystring)
            result.raise_for_status()
            return result.json()["results"]
        except (requests.RequestException, ValueError):
            print("Сетевая ошибка")
            return False

    @classmethod
    def get_recipe_ingredients(cls, recipe_id):
        url = cls.base_url + str(recipe_id) + "/information"
        querystring = {
            "apiKey": SPOONACULAR_API_KEY,
            "id": recipe_id,
        }
        try:
            result = requests.get(url, headers=cls.headers, params=querystring)
            result.raise_for_status()
            return result.json()["extendedIngredients"]
        except (requests.RequestException, ValueError):
            print("Сетевая ошибка")
            return False


if __name__ == "__main__":
    print(
        get_translation(["cow"], source_language_code="en", target_language_code="ru")
    )
