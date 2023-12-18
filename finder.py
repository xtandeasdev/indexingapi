import requests
import json
from bs4 import BeautifulSoup

from colorama import Fore, Back, Style, init

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


keys = input("keys: ")
keys = keys.split(",")
site = input("site: ")
pages = int(input("page: "))
pages = (pages + 1) * 10
f = open("{}.txt".format(site), "w")
f.flush()
for key in keys:
    sira = 0
    bulundu = False
    for i in range(pages):
        if i % 10 == 0:
            params = {"q": key, "gl": "tr", "hl": "tr", "start": i}
            response = requests.get(
                "https://www.google.com/search", params=params, headers=headers
            )
            if response.status_code == 429:
                print(Fore.BLUE+"Çok fazla istekten dolayı google engelledi.")
                break
            soup = BeautifulSoup(response.text, "html.parser")
            for result in soup.select(".tF2Cxc"):
                sira += 1
                title = result.select_one(".DKV0Md").text
                link = result.select_one(".yuRUbf a")["href"]
                if str.find(link, site) > 1:
                    bulundu = True
                    text = "{} siteniz {} keyinde {} sırada bulundu.\n".format(
                        link, key, sira
                    )
                    print(Fore.WHITE+text)
                    f.write("{}\n".format(text))
                else:
                    text = "{} sitesi {} keyinde {}. sırada bulundu.".format(
                        link, key, sira
                    )
                    print(
                        Fore.RED+
                            text
                    )
                    f.write("{}\n".format(text))

    if bulundu == False:
        text = "{} Siteniz {} keyinde maalesef bulunamadı.\n".format(site, key)
        print(text)
        f.write("{}\n".format(text))
