import requests
from const import user_agent
from functions import get_html, BeautifulSoup, get_ip


def update() -> any:
    if input("Обновить список юзер агентов и прокси?[y/n]:") == "y":
        result: list = []
        url_proxy: str = "https://hidemy.name/ru/proxy-list/?maxtime=1400&type=h&anon=34&start=#list"
        page_proxy: requests = get_html(url_proxy.replace("start=", "start=0"), user_agent)
        if page_proxy.status_code == 200:
            quantity_page: int = len((BeautifulSoup(page_proxy.text, 'lxml').find("div", class_="pagination")).find_all("li")) - 1
            for i in range(quantity_page):
                if page_proxy.status_code == 200:
                    list_proxy: list = (BeautifulSoup(page_proxy.text, "lxml").find("table")).find_all("tr")
                    del list_proxy[0]
                    for tr in list_proxy:
                        ip = tr.find_all("td")
                        result.append(get_ip(ip[4].text.lower(), ip[0].text, ip[1].text))
                page_proxy = get_html(url_proxy.replace("start=", "start=" + str(64 * (i + 1))), user_agent)
        with open("proxy.txt", "w+") as file:
            for i in result:
                try:
                    file.write(str(i['http']) + "\n")
                except Exception as KeyError:
                    print(KeyError)
            file.close()
        url_ua: str = "https://seolik.ru/user-agents-list"
        page_ua = get_html(url_ua, user_agent)
        list_user_agent = (BeautifulSoup(page_ua.text, "lxml").find("div", class_="table-responsive")).find_all("tr")
        with open("ua.txt", "w+") as file:
            for i in list_user_agent:
                file.write(i.find_all("td")[1].text + "\n")
