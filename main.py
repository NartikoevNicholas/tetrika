import time
from update_proxy_useragent import update
from multiprocessing import Pool
from const import tests, alphabet_list, url_wikipedia
from functions import *


def task(array: str) -> int:
    len_array: int = len(array)
    h: int = get_index(len_array)
    h_temp: int = 0
    while True:
        if array[h] == "1":
            if array[h + 1] == "0":
                return h + 1
            h_temp = h
            h += get_index(len_array - h)
        else:
            if array[h - 1] == "1":
                return h
            h -= get_index(h - h_temp)


def handler(character) -> str:
    proxy_list: list = open("proxy.txt").read().split("\n")
    ua_list: list = open("ua.txt").read().split("\n")
    result: list = get_data(url_wikipedia.replace("from=", f"from={character}"), proxy_list, ua_list)
    return f"{character}: {len(result)}"


def appearance(intervals) -> int:
    result: int = 0
    list_lesson: list = get_list(intervals['lesson'])
    list_pupil: list = get_list(intervals['pupil'])
    list_tutor: list = get_list(intervals['tutor'])

    for _ in range(len(list_lesson)):
        if list_pupil.__contains__(list_lesson[_]) and list_tutor.__contains__(list_lesson[_]):
            result += 1
    return result


if __name__ == '__main__':
    # Задача №1.
    # Дан массив чисел, состоящий из некоторого количества подряд идущих единиц,
    # за которыми следует какое-то количество подряд идущих нулей: 111111111111111111111111100000000
    print("Задача №1")

    count_one: int = 2324323200
    count_zero: int = 999999999
    # массив единиц и нулей -> string
    array_string = get_array(count_one, count_zero)
    print(f"Массив длиной элементов {count_one + count_zero}, "
          f"где количество единиц равно {count_one}, а нулей {count_zero}.")

    # мое решение
    start = time.time()
    index: int = task(array_string)
    end = time.time()
    print(f"Мое решение: {index}. Время: {end - start}")

    # решение python
    start = time.time()
    index: int = array_string.index("0")
    end = time.time()
    print(f"Решение python: {index}. Время: {end - start}")

    # Задача №2.
    # Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) и вывести количество животных на
    # каждую букву алфавита. Результат должен получиться в следующем виде:
    # А: 642
    # Б: 412
    # В:....
    print("Задача №2")

    update()
    with Pool(16) as pool:
        result_list: list = pool.map(handler, alphabet_list)
    for el in result_list:
        print(el)

    # Задача №3
    # Мы сохраняем время присутствия каждого пользователя на уроке в виде интервалов. В функцию передается словарь,
    # содержащий три списка с таймстемпами (время в секундах):
    # lesson – начало и конец урока
    # pupil – интервалы присутствия ученика
    # tutor – интервалы присутствия учителя
    # Интервалы устроены следующим образом – это всегда список из четного количества элементов. Под четными индексами
    # (начиная с 0) время входа на урок, под нечетными - время выхода с урока.
    # Нужно написать функцию, которая получает на вход словарь с интервалами и возвращает время общего присутствия
    # ученика и учителя на уроке (в секундах).
    print("Задача №3")

    start = time.time()
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    end = time.time()
    print(end - start)
