import os
import platform
import json

# ger "\\" om os är windows och "/" om os är unix-baserat
def determineslash():
    os = (platform.system()).lower()
    if "windows" == os:
        return "\\"
    else:
        return "/"

slash = determineslash()

def init():
    #Kollar om konfiguretionsfilen config.json finns annars skapas den
    if os.path.exists(os.getcwd() + slash + "config.json"):
        pass
    else:
        dict = []
        blacklists = ["config_files" + slash + "blacklist.txt", "config_files" + slash + "blacklist2.txt" ]
        whitelists = ["config_files" + slash + "whitelist.txt"]
        wordlists = ["config_files" + slash + "wordlist.txt"]
        localaddresslists = ["config_files" + slash + "localaddresses.txt"]
        publicdnsservers= ["8.8.8.8", "8.8.4.4"]
        dict.append({'Blacklists': blacklists, 'Whitelists': whitelists,'Wordlists': wordlists,
                     'Localaddresslists': localaddresslists, 'Public_DNS_servers': publicdnsservers})

        with open("config.json", "w+", encoding="utf-8") as configfile:
            json.dump(dict, configfile, indent=2)
        configfile.close()

def getfromjson(list):
    #Hämtar värden från config.json
    with open("config.json", "r") as cf:
        configdata = json.load(cf)
    cf.close()

    data = configdata[0][list]
    print(list, data)
    return data

#getfromjson('Public_DNS_servers')