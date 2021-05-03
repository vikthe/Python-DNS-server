from DNS import DNSrequest
import socket
import configurations as DNSconfig
DNSconfig.init()
import time

import threading
from flask import Flask, render_template, request
app = Flask(__name__)

#this is the flask website server
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/statistics/")
def rootstats():
    return render_template("index.html")

@app.route("/statistics/<statstype>/", methods = ["POST", "GET"])
@app.route("/statistics/<statstype>", methods = ["POST", "GET"])
def stats(statstype):
    #handles listchanges
    if statstype == "speedtest":
        pass
    return render_template("index.html")

@app.route("/configurations/")
def rootconfig():
    return render_template("index.html")

@app.route("/configurations/<configtype>/", methods = ["POST", "GET"])
@app.route("/configurations/<configtype>", methods = ["POST", "GET"])
def config(configtype):
    #handles listchanges
    if configtype in ["blacklist", "whitelist", "localaddresslist", "wordlist"]:
        listarray = DNSconfig.getfromjson(configtype + "s")
        if request.method == 'POST':
            form = request.form
            if "action" in form and "value" in form:
                action = form["action"]
                value = form["value"]
                DNSconfig.setlist(listarray, action, value)
    return render_template("index.html")

@app.route("/configurations/data", methods = ["POST", "GET"])
#to send get responses with data to client
def getconfigdata():
    args = request.args
    if "getlist" in args:
        listarray = DNSconfig.getfromjson(args["getlist"])
        alllistentries = DNSconfig.getfromlist(listarray)
        print("allist", alllistentries)
        dict = {0:alllistentries}
        return dict

#to handle errors such as wrong url
@app.errorhandler(Exception)
def error(e):
    return render_template("error.html", errormessage = e)


if __name__ == "__main__":
    #debug = True does not work
    t = threading.Thread(target=app.run)
    t.start()

#this is the DNS server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ''
port = 53
size = 512
s.bind((host,port))

while True:
    #start = time.time() * 1000
    data , addr = s.recvfrom(size)
    start = time.time()*1000

    print("Raw request", data)

    req = DNSrequest(data)
    print("Domainname", req.domainname)

    ip, addresstype = DNSconfig.checkdomainname(req.domainname)
    print(ip, addresstype)

    if addresstype == "local":
        response = req.getlocalresponse(ip, 3600)

    elif addresstype == "public":
        response = req.getpublicresponse()

    print("Response", response)
    s.sendto(response, addr)
    print(time.time()*1000 - start)
