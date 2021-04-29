from DNS import DNSrequest
import socket
import configurations as DNSconfig
DNSconfig.init()
import time

import threading
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

#this is the flask website server
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/statistics/")
def rootstats():
    return render_template("index.html")

@app.route("/configurations/")
def rootconfig():
    return render_template("index.html")

@app.route("/statistics/speedtest/")
def statsspeedtest():
    return render_template("index.html")

@app.route("/configurations/blacklist/", methods = ["POST", "GET"])
def configblacklist():
    blacklistarray = DNSconfig.getfromjson("Blacklists")
    alllistentries = DNSconfig.getfromlist(blacklistarray)
    print(alllistentries)
    if request.method == 'POST':
        form = request.form
        if "action" in form and "value" in form:
            action = form["action"]
            value = form["value"]
            DNSconfig.setlist(blacklistarray, action, value)
    return render_template("index.html", data = alllistentries)

@app.route("/configurations/whitelist/", methods = ["POST", "GET"])
def configwhitelist():
    whitelistarray = DNSconfig.getfromjson("Whitelists")
    alllistentries = DNSconfig.getfromlist(whitelistarray)
    print(alllistentries)
    if request.method == 'POST':
        form = request.form
        if "action" in form and "value" in form:
            action = form["action"]
            value = form["value"]
            DNSconfig.setlist(whitelistarray, action, value)
            DNSconfig.setlist(whitelistarray, action, value)
    return render_template("index.html", data = alllistentries)

@app.errorhandler(Exception)
def error(e):
    return render_template("error.html", errormessage = e)


if __name__ == "__main__":
    t = threading.Thread(target=app.run(debug=True))
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
