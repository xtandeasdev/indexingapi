import argparse
import requests
from updater import update
import sys
import os
systems = "Indexing\nFinder"
dirs = os.listdir()
def check_connection():
    try: 
        r = requests.get("https://www.google.com",timeout=10)
        return True
    except:
        return False
if check_connection() == False:
    print("Bu programı kullanabilmek için internet bağlantısına ihtiyacınız var.")
    exit()
check_updates = input("Güncellemeleri denetlemek istiyor musunuz? (E/H): ")
if check_updates.lower() == "y" or check_updates.lower() == "e" or check_updates.lower() == "yes" or check_updates.lower() == "evet":
    for dir in dirs:
        update(dir)
elif check_updates.lower() == "n" or check_updates.lower() == "h" or check_updates.lower() == "no" or check_updates.lower() == "hayır":
    print("Güncellemeler denetlenmiyor.")
    
if len(sys.argv) >= 2:
    file = os.path.isfile(sys.argv[1]+".py")
    if file:
        exec(open(sys.argv[1]+".py", "r", encoding="utf-8").read())
    else:
        print("Böyle bir sistem bulunmamakta hangisi kullanmak istemiştiniz?\n"+systems)
else:
    print("Bir sistem seçmek zorundasınız örn. python index.py indexing\nSistemler: "+systems)
