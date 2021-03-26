import os
import json

def init():
    #checks if konfiguretionfile config.json exist and creates new if it doesnt
    print(os.getcwd() + os.sep + "config.json")
    if os.path.exists(os.getcwd() + os.sep + "config.json"):
        print(os.getcwd() + os.sep + "config.json", "exists move on")
    else:
        dict = []
        blacklists = ["config_files" + os.sep + "blacklist.txt"]
        whitelists = ["config_files" + os.sep + "whitelist.txt"]
        wordlists = ["config_files" + os.sep + "wordlist.txt"]
        localaddresslists = ["config_files" + os.sep + "localaddresslist.txt"]
        publicdnsservers= ["8.8.8.8", "8.8.4.4"]
        dict.append({'Blacklists': blacklists, 'Whitelists': whitelists,'Wordlists': wordlists,
                     'Localaddresslists': localaddresslists, 'Public_DNS_servers': publicdnsservers})

        with open("config.json", "w+", encoding="utf-8") as configfile:
            json.dump(dict, configfile, indent=2)
        configfile.close()


    if os.path.exists(os.getcwd() + os.sep + "config_files"):
        #checks if folder config_files exists and creates it if it doesnt
        pass
    else:
        os.mkdir(os.getcwd() + os.sep + "config_files")


    def checkandcreatefiles(file, message):
        #creates examplefiles if the dont exist
        path = os.getcwd() + os.sep + "config_files" + os.sep + file
        if os.path.exists(path):
            pass
        else:
            with open(path, "w+") as f:
                f.write(message)
            f.close()

    checkandcreatefiles("blacklist.txt", "#Blocks specified domain, example: \n#0.0.0.0 youtube.com")
    checkandcreatefiles("localaddresslist.txt", "#Add addresses in a local network, example: \n#192.168.1.10 my.website.com")
    checkandcreatefiles("whitelist.txt", "Add domains you want to whitelist from wordlist or/and blacklist, example:\n#youtube.com")
    checkandcreatefiles("wordlist.txt", "#Domainnames with these words included in are blocked, example: \n#ad, ads, word, hello")


def getfromjson(list):
    #returns values from config.json as an array
    with open("config.json", "r") as cf:
        configdata = json.load(cf)
    cf.close()

    data = configdata[0][list]
    print(list, data)
    return data

def setjson(category, action, value):
    #function to change json file (used by flask app)
    pass

def setlist(list, action, value):
    #function to change or set value in lists (blacklist, whitelist etc)
    pass


def checkdomainname(domainname):
    def iscomment(line):
        #kollar om raden är utkommenterad eller ej
        if line[0] == "#":
            return True
        else:
            return False

    def checklists(listarray, listtype):
        for list in listarray:
            with open(list, "r") as lf:
                if listtype == "blacklist":
                    for line in lf:
                        if domainname == line.split()[1] and not iscomment(line):
                            return True

                elif listtype == "wordlist":
                    for line in lf:
                        if not iscomment(line):
                            words = line.split(",")
                            for word in words:
                                if word == domainname:
                                    return True

                elif listtype == "whitelist":
                    for line in lf:
                        if line == domainname and not iscomment(line):
                            return True

                elif listtype == "locallist":
                    for line in lf:
                        if domainname == line.split()[1] and not iscomment(line):
                            return line.split()[0]

        return False


    blacklistcheck = checklists(getfromjson('Blacklists'), "blacklist")
    whitelistcheck = checklists(getfromjson('Whitelists'), "whitelist")
    if blacklistcheck and not whitelistcheck:
        #returns 0.0.0.0 if blacklisted while not whitelisted, if not it checks if domainname is in wordlist or locallist
        return "0.0.0.0", "local"

    else:
        wordlistcheck = checklists(getfromjson('Wordlists'), "wordlist")
        if wordlistcheck and not whitelistcheck:
            #if domainname is blocked by wordlist and not in whitelist function returns 0.0.0.0
            return "0.0.0.0", "local"

        else:
            #if domainame not blocked yet it checks localaddresslist
            locallistcheck = checklists(getfromjson('Localaddresslists'), "locallist")
            if locallistcheck:
                return locallistcheck, "local"

            else:
                #last resort is to send it to public dns-server
                return None, "public"
