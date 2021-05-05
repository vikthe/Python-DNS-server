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
        dict.append({'blacklists': blacklists, 'whitelists': whitelists,'wordlists': wordlists,
                     'localaddresslists': localaddresslists, 'public_DNS_servers': publicdnsservers})

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

    checkandcreatefiles("blacklist.txt", "#Blocks specified domain, example: \n#youtube.com")
    checkandcreatefiles("localaddresslist.txt", "#Add addresses in a local network, example: \n#192.168.1.10 my.website.com")
    checkandcreatefiles("whitelist.txt", "Add domains you want to whitelist from wordlist or/and blacklist, example:\n#youtube.com")
    checkandcreatefiles("wordlist.txt", "#Domainnames with these words included in are blocked, example: \n#ad, ads, word, hello")


def getfromjson(list):
    #returns values from config.json as an array
    try:
        with open("config.json", "r") as cf:
            configdata = json.load(cf)
        cf.close()

        data = configdata[0][list]
        print(list, data)
        return data

    except FileNotFoundError:
        print("FileNotFoundError: config.json doesn't exists")

def setjson(category, action, value):
    #function to change json file (used by flask app)
    try:
        with open("config.json", "r") as cf:
            configdata = json.load(cf)
            categorydata = configdata[0][category]
        cf.close()

        if action == "add":
            categorydata.append("config_files" + os.sep + value)

        elif action == "remove":
            for item in categorydata:
                if item.split(os.sep)[-1] == value:
                    categorydata.remove(item)

        with open("config.json", "w") as cf:
            json.dump(configdata, cf, indent=2)
        cf.close()

    except FileNotFoundError:
        print("FileNotFoundError: config.json doesn't exists")
    except KeyError:
        print("KeyError: Category not found")


def setlist(listarray, action, value):
    #function to change or set value in lists (blacklist, whitelist etc)
    if action == "add":
        firstlist = listarray[0]
        print("Configurations: setlist", firstlist)
        with open(firstlist, "a") as lf:
            lf.write( "\n" + value)
        lf.close()

    elif action == "remove":
        for list in listarray:
            linelist = []
            print(list)
            with open(list, "r") as lf:
                for line in lf:
                    if line.strip() != value and line != '' and line != '\n':
                            linelist.append(line)
            lf.close()
            with open(list, "w") as lf:
                print("linelist", linelist)
                lf.writelines(linelist)
            lf.close()

    elif action == "clear":
        for list in listarray:
            print(list)
            with open(list, "w") as lf:
                lf.write("")
            lf.close()

#get all values from a list type. example get all values from all blacklists
def getfromlist(listarray):
    completelist = []
    for list in listarray:
        print(list)
        with open(list, "r") as lf:
            for line in lf:
                if line != '' and line != '\n':
                    completelist.append(line)
    return completelist

#a function to check if the domainname should be blocked or not
def checkdomainname(domainname):
    domainname = domainname.lower()
    def iscomment(line):
        #checks if line is a comment
        if line != "":
            if line[0] == "#":
                return True
            else:
                return False

    #goes through all lists
    def checklists(listarray, listtype):
        for list in listarray:
            with open(list, "r") as lf:
                if listtype == "blacklist":
                    for line in lf:
                        line = line.strip()
                        if len(line.split()) >= 2 and not iscomment(line):
                            if domainname == line.split()[1].lower():
                                return True
                        elif len(line.split()) == 1 and not iscomment(line):
                            if domainname == line:
                                return True

                elif listtype == "wordlist":
                    for line in lf:
                        line = line.strip()
                        if not iscomment(line):
                            words = line.split(",")
                            for word in words:
                                if domainname ==  word.lower():
                                    return True

                elif listtype == "whitelist":
                    for line in lf:
                        line = line.strip()
                        if domainname == line.lower() and not iscomment(line):
                            return True

                elif listtype == "locallist":
                    for line in lf:
                        line = line.strip()
                        if domainname == line.split()[1].lower() and not iscomment(line):
                            return line.split()[0].lower()

        return False


    blacklistcheck = checklists(getfromjson('blacklists'), "blacklist")
    whitelistcheck = checklists(getfromjson('whitelists'), "whitelist")
    if blacklistcheck and not whitelistcheck:
        #returns 0.0.0.0 if blacklisted while not whitelisted, if not it checks if domainname is in wordlist or locallist
        return "0.0.0.0", "local"

    else:
        wordlistcheck = checklists(getfromjson('wordlists'), "wordlist")
        if wordlistcheck and not whitelistcheck:
            #if domainname is blocked by wordlist and not in whitelist function returns 0.0.0.0
            return "0.0.0.0", "local"

        else:
            #if domainame not blocked yet it checks localaddresslist
            locallistcheck = checklists(getfromjson('localaddresslists'), "locallist")
            if locallistcheck:
                return locallistcheck, "local"

            else:
                #last resort is to send it to public dns-server
                return None, "public"
