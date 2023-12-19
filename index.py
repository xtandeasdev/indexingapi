import argparse
import requests

import sys
import os
systems = "Indexing\nFinder"

def check_connection():
    try: 
        r = requests.get("https://www.google.com",timeout=10)
        return True
    except:
        return False
if check_connection() == False:
    print("Bu programı kullanabilmek için internet bağlantısına ihtiyacınız var.")
    exit()
if len(sys.argv) >= 2:
    file = os.path.isfile(sys.argv[1]+".py")
    if file:
        exec(open(sys.argv[1]+".py", "r", encoding="utf-8").read())
    else:
        print("Böyle bir sistem bulunmamakta hangisi kullanmak istemiştiniz?\n"+systems)
else:
    print("Bir sistem seçmek zorundasınız örn. python index.py indexing\nSistemler: "+systems)
