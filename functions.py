import math
import requests
from const import url_main
from random import choice
from bs4 import BeautifulSoup
from urllib.parse import unquote


# Функция, которая возвращает строку с единицами и нулями, где кол-е единиц равное "count_one", а нулей "count_zero"
def get_array(count_one: int, count_zero: int) -> str:
    return "1" * count_one + "0" * count_zero


# Функция, которая принимает целое число и возвращает целое число деленное на 2
def get_index(h: int) -> int:
    return math.ceil(h / 2)


# Функция, которая преобразует что-то в список строк с порядковым номером
def get_list(data_list: list, count: int = 0) -> list:
    result: list = []
    if count != 0:
        for i in range(count):
            result.append(str(data_list[0] + i))
        return result
    else:
        for i in range(int(len(data_list)/2)):
            for j in range(data_list[(i * 2) + 1]-data_list[i*2]):
                result.append(str(data_list[i*2] + j))
        return result


# Функция, которая получает html страницу
def get_main_html(url, proxy_list: list, ua_list: list) -> requests:
    while True:
        proxy: str = choice(proxy_list)
        ua: str = choice(ua_list)
        proxies: dict = {'http': 'http://' + proxy}
        headers: dict = {'User-Agent': ua}
        result: requests = get_html(url, headers, proxies)
        if result is not None and result.status_code == 200:
            return result


def get_data(url: str) -> dict:
    result = {}
    while True:
        html = get_html(url)
        soup = BeautifulSoup(html.text, 'lxml')
        list_animals = soup.find_all("div", class_="mw-content-ltr")[-1].find("ul").find_all("li")
        for animal in list_animals:
            if animal.text[0] == "A": # "A" - английская буква
                return result
            if result.keys().__contains__(animal.text[0]) is False:
                result[animal.text[0]] = 1
            else:
                result[animal.text[0]] += 1
        url = url_main + unquote(soup.find("a", text="Следующая страница")['href'])


# вспомогательная функция
def get_html(url, headers=None, proxies=None):
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response
        else:
            return None
    except Exception as ex:
        print(ex)


# вспомогательная функция
def get_ip(protocol: str, ip: str, port: str) -> dict:
    result: dict = {}
    if protocol == "http":
        result["http"] = ip + ":" + port
    return result
