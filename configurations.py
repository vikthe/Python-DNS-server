import os
import platform
import json

#returns "\\" if os is windows and "/" if os is unix-based
def determineslash():
    os = (platform.system()).lower()
    if "windows" == os:
        return "\\"
    else:
        return "/"


def init():
    slash = determineslash()

    #checks if konfiguretionfile config.json exist and creates new if it doesnt
    print(os.getcwd() + slash + "config.json")
    if os.path.exists(os.getcwd() + slash + "config.json"):
        print(os.getcwd() + slash + "config.json", "exists move on")
    else:
        print("Hi")
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


    #checks if folder config_files exists and creates it if it doesnt
    print(os.getcwd() + slash + "config_files")
    if os.path.exists(os.getcwd() + slash + "config_files"):
        pass
    else:
        os.mkdir(os.getcwd() + slash + "config_files")

    #creates examplefiles if the dont exist
    def checkandcreatefiles(file, message):
        path = os.getcwd() + slash + "config_files" + slash + file
        if os.path.exists(path):
            pass
        else:
            with open(path, "w+") as f:
                f.write(message)
            f.close()

    checkandcreatefiles("blacklist.txt", "#Blocks specified domain, example: \n#0.0.0.0 www.youtube.com")
    checkandcreatefiles("localaddresslist.txt", "#Add addresses in a local network, example: \n#192.168.1.10 my.website.com")
    checkandcreatefiles("whitelist.txt", "Add domains you want to whitelist from wordlist or/and blacklist, example:\n#youtube.com")
    checkandcreatefiles("wordlist.txt", "#Domainnames with these words included in are blocked, example: \n#ad, ads, word, hello")


def getfromjson(list):
    #returns values from config.json
    with open("config.json", "r") as cf:
        configdata = json.load(cf)
    cf.close()

    data = configdata[0][list]
    print(list, data)
    return data
