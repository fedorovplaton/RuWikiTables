import requests
from bs4 import BeautifulSoup
import pandas as pd


# Скрипт для получения того, сколько всего страниц в русской вики
# Заходит на сайт со статистикой, наход таблицу со статистикой (Она первая)
# Находим там строку про русскую вики
# И берет оттуда просто число
def get_ru_titles_total_count() -> int:
    response = requests.get("https://ru.wikipedia.org/wiki/Служебная:Статистика")
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table', {'class': "wikitable"})
    df = pd.read_html(str(indiatable))
    df = pd.DataFrame(df[0])
    value: str = ''.join(df.loc[1]['Статистика по страницам.1'].split())

    return int(value)
