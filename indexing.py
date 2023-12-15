import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os
import time
import sys
from colorama import Fore, Back, Style, init
import argparse
parser = argparse.ArgumentParser(description="IndexingApi")
init(autoreset=True)
parser.add_argument("-s", "--Site", help="Example: site ", required=False, default="")
parser.add_argument(
    "-u",
    "--Update",
    help="Example:  [1]Url Updated or [2]Url Deleted ",
    required=True,
    default="",
)
parser.add_argument(
    "-c", "--Count", help="Example:  Only one url ", required=False, default="none"
)
parser.add_argument(
    "-f", "--File", help="İçindeki siteleri indexletmek için dosya yolunu giriniz.", required=False
)
parser.add_argument(
    "-o", "--Output", help="Indexlenen siteleri yazdırmak istediğiniz dosya adı.", required=False
)
argument = parser.parse_args(sys.argv[2:])
website_url = argument.Site
updated = argument.Update
count = argument.Count
filepath = argument.File
output = argument.Output
try:
    fileurls = set()
    domain = urlparse(website_url).netloc
    if filepath:
        print("Dosya içindeki websiteler taranıyor.")
        if os.path.isfile(filepath):
            file = open(filepath, "r")
            if file.readable():
                lines = file.readlines()
                count = 0
                for line in lines:
                    count += 1
                    website_url = line
                    domain = urlparse(line)
                    if domain.netloc:
                        domain = domain.netloc
                        print(Fore.RED+line)
                        fileurls.add(line)
                    else:
                        print("{}. satırdaki website formata uygun değil.".format(count))
                
            else:
                print("Dosya okunamıyor lütfen izinleri kontrol edin.") 
        else:
            print("Lütfen doğru bir dosya yolu giriniz.")
    getUrls = set()
    def get_all_urls(base_url):
        if base_url not in getUrls:
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, "html.parser")
            anchor_tags = soup.find_all("a")
            urls = set()
            for tag in anchor_tags:
                href = tag.get("href")
                if href is not None:
                    hrefnetloc = urlparse(href).netloc
                    if hrefnetloc == domain:
                        url = urljoin(base_url, href)
                        urls.add(url)

            return urls
    jsonname = website_url[8:]
    if str.startswith(jsonname, "www."):
        jsonname = website_url[12:]

    jsonfilename = str.split(jsonname, "/")[0]
    jsonfilename = str.split(jsonfilename, ".")
    jsonfilename = "".join(jsonfilename)
    JSON_KEY_FILE = "./apis/{}.json".format(jsonfilename)
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        JSON_KEY_FILE, scopes=SCOPES
    )
    http = credentials.authorize(httplib2.Http())

    def indexURL(urls, http):
        if output:
            file = open(output, "w")
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

        for u in urls:
            content = {}
            content["url"] = u.strip()
            if updated == "2":
                content["type"] = "URL_DELETED"
            else:
                content["type"] = "URL_UPDATED"
            json_ctn = json.dumps(content)

            response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

            result = json.loads(content.decode())

            if "error" in result:
                print(
                    "Error({} - {}): {}".format(
                        result["error"]["code"],
                        result["error"]["status"],
                        result["error"]["message"],
                    )
                )
            else:
               if updated == "2":
                    print(
                    "Gönderilen URL: {}".format(
                        result["urlNotificationMetadata"]["url"]
                        )
                    )
                    print(
                        Back.GREEN
                        + Fore.WHITE
                        + "Indexlenen Url: {}".format(
                            result["urlNotificationMetadata"]["latestRemove"]["url"]
                        )
                    )
                    print(
                        Back.GREEN
                        + Fore.WHITE
                        + "Indexleme Türü: URL_SILINDI"
                    )
                    print(
                        Back.GREEN
                        + Fore.WHITE
                        + "Indexlenme Zamanı: {}".format(
                            result["urlNotificationMetadata"]["latestRemove"]["notifyTime"]
                        )
                    )
                    if output:
                        
                        file.writelines("Gönderilen URL: {}\n".format(
                            result["urlNotificationMetadata"]["url"]
                        ))
                        file.writelines("Indexlenen URL: {}\n".format(
                            result["urlNotificationMetadata"]["latestRemove"]["url"]
                        ))
                        file.writelines("Indexlenme Türü: URL_SILINDI\n")
                        file.writelines("Indexlenme Zamanı: {}\n".format(
                            result["urlNotificationMetadata"]["latestRemove"]["notifyTime"]
                        ))
                        file.writelines("\n")
                        
                        

               elif updated == "1":
                    print(
                    "Gönderilen URL: {}".format(
                        result["urlNotificationMetadata"]["url"]
                        )
                    )
                    print(
                        Back.GREEN
                        + Fore.WHITE
                        + "Indexlenen URL: {}".format(
                            result["urlNotificationMetadata"]["latestUpdate"]["url"]
                        )
                    )
                    print(
                        Back.GREEN
                        + Fore.WHITE
                        + "Indexlenme Türü: URL_EKLENDI"
                    )
                    print(
                        Back.GREEN
                        + Fore.WHITE
                        + "Indexlenme Zamanı: {}".format(
                            result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]
                        )
                    )
                    if output:
                        file.writelines("Gönderilen URL: {}\n".format(
                            result["urlNotificationMetadata"]["url"]
                        ))
                        file.writelines("Indexlenen URL: {}\n".format(
                            result["urlNotificationMetadata"]["latestUpdate"]["url"]
                        ))
                        file.writelines("Indexlenme Türü: URL_EKLENDI\n")
                        file.writelines("Indexlenme Zamanı: {}\n".format(
                            result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]
                        ))
                        file.writelines("\n")
                        
        if output:
            print(output + " isimli dosyaya indexlenen site bilgileri yazıldı.")
                    
               

    if count == "true":
        indexURL([website_url], http)
        print("Bir tane url indexlendi.")
        time.sleep(1)
        print(
        Back.WHITE
        + Fore.BLACK
        + "İndexleme işlemi bitti. Bizi kullandığınız için teşekkür ederiz."
    )
        exit()
    
    if len(fileurls) > 0:
        indexURL(fileurls, http)
        exit()
    all_urls = get_all_urls(website_url)
    for url in all_urls:
        if url is not None:
            all = get_all_urls(url)
            getUrls.add(url)
            if all is not None:
                for url in all:
                    if url is not None:
                        if url not in getUrls:
                            getUrls.add(url)
                            all = get_all_urls(url)
                            if all is not None:
                                for url in all:
                                    if url is not None:
                                        if url not in getUrls:
                                            getUrls.add(url)
                                            for url in all:
                                                if url is not None:
                                                    if url not in getUrls:
                                                        getUrls.add(url)
                                                        for url in all:
                                                            if url is not None:
                                                                if url not in getUrls:
                                                                    getUrls.add(url)
    print(Fore.WHITE + "Bütün urller tarandı.")
    time.sleep(2)
    for url in getUrls:
        print(Fore.RED + url)
    time.sleep(2)
    indexURL(getUrls, http)
    print(
        Back.WHITE
        + Fore.BLACK
        + "İndexleme işlemi bitti. Bizi kullandığınız için teşekkür ederiz."
    )
    time.sleep(1)
except Exception as e:
    print(e)
