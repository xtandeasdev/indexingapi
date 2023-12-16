import requests
import os
def get_file(file_name):
    print(file_name)
    req = requests.get("https://raw.githubusercontent.com/xtandeasdev/indexingapi/main/"+file_name)
    return req
def exists(file_name):
    file = get_file(file_name)
    if file.status_code == 200:
        return True
    else:
        return False
def is_stable(file_name):
    file = get_file(file_name)
    if exists(file_name):
        localfile = open(file_name, "r", encoding="utf-8")
        if localfile.readable():
            if file.text == localfile.read():
                return True
            else:
                return False
    return False
def update(file_name):
    isexists = exists(file_name)
    if isexists:
        file = get_file(file_name)
        if is_stable(file_name):
            print(file_name+" Güncel")
        else:
            print(file_name+" repo ile eşitleniyor. Lütfen terminali kapatmayın.")
            localfile = open(file_name, "w", encoding="utf-8")
            localfile.flush()
            localfile.write(file.text.encode("utf-8").decode("utf-8"))
