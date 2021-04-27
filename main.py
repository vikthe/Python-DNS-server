from DNS import DNSrequest
import socket
import configurations as DNSconfig
DNSconfig.init()

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
def stats():
    return render_template("index.html")

@app.route("/configurations/blacklist/", methods = ["POST", "GET"])
def config():
    if request.method == 'POST':
        #print("Hej")
        form = request.form
        print(form)
        print("Action", form["action"])
        print(form)
        if "action" in form:
            print("Action", form["action"])
    return render_template("index.html")

@app.errorhandler(Exception)
def error(e):
    return render_template("error.html", errormessage = e)


if __name__ == "__main__":
    t = threading.Thread(target=app.run)
    t.start()


#this is the DNS server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ''
port = 53
size = 512
s.bind((host,port))

while True:
    data , addr = s.recvfrom(size)
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



