import argparse
from updater import update
import sys
import os
systems = "Indexing\nFinder"
dirs = os.listdir()
for dir in dirs:
    update(dir)
file = os.path.isfile(sys.argv[1]+".py")
if sys.argv[1]:
    if file:
        exec(open(sys.argv[1]+".py", "r", encoding="utf-8").read())
    else:
        print("Böyle bir sistem bulunmamakta hangisi kullanmak istemiştiniz?\n"+systems)
else:
    print("Bir sistem seçmek zorundasınız örn. python index.py indexing\nSistemler: "+systems)
