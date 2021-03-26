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
    #returns values from config.json
    with open("config.json", "r") as cf:
        configdata = json.load(cf)
    cf.close()

    data = configdata[0][list]
    print(list, data)
    return data

def setjson():
    #set values to json
    pass

def checkdomainname(self):
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
                        if self.domainname == line.split()[1] and not iscomment(line):
                            return True

                elif listtype == "wordlist":
                    for line in lf:
                        if not iscomment(line):
                            words = line.split(",")
                            for word in words:
                                if word == self.domainname:
                                    return True

                elif listtype == "whitelist":
                    for line in lf:
                        if line == self.domainname and not iscomment(line):
                            return True

                elif listtype == "locallist":
                    for line in lf:
                        if self.domainname == line.split()[1] and not iscomment(line):
                            return line.split()[0]

        return False


    blacklistarray = config.getfromjson('Blacklists')
    print(blacklistarray)
    blacklistcheck = checklists(blacklistarray, "blacklist")

    whitelistarray = config.getfromjson('Whitelists')
    whitelistcheck = checklists(whitelistarray, "whitelist")

    if blacklistcheck and not whitelistcheck:
        #om den är blacklistad och inte whitelistad returnas 0.0.0.0 annars kollas om den är med i wordlist eller locallist
        print("Blacklisted", self.domainname)
        return "0.0.0.0", "local"

    else:
        wordlistarray = config.getfromjson('Wordlists')
        wordlistcheck = checklists(wordlistarray, "wordlist")
        if wordlistcheck and not whitelistcheck:
            #om den blir blockad i wordlist och inte finns med i whitelist ska det returna 0.0.0.0
            return "0.0.0.0", "local"

        else:
            #om den inte är blockad än kollas localaddresslist
            locallistarray = config.getfromjson('Localaddresslists')
            locallistcheck = checklists(locallistarray, "locallist")
            if locallistcheck:
                return locallistcheck, "local"

            else:
                #sista utvägen är att skicka till publik DNS
                return None, "public"
