from DNS import DNSresponse, DNSrequest

import os
import socket
import configurations as DNSconfig
DNSconfig.init()

import threading
from flask import Flask, render_template, request
app = Flask(__name__)

from werkzeug.utils import secure_filename
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "config_files"
allowed_filetypes = ['txt']

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
    if statstype == "speedtest":
        pass
    return render_template("index.html")

@app.route("/statistics/data", methods = ["POST", "GET"])
#dns "api"
def getstatsdata():
    args = request.args
    print(args)
    if "resolvename" in args:
        ip, addresstype = DNSconfig.checkdomainname(args["resolvename"])
        print(ip, addresstype)
        if addresstype == "local":
            dict = {"Answer":[{"data":ip}]}
            return dict
        elif addresstype == "public":
            req = DNSrequest(args["resolvename"])
            dnsrequest = req.createrequest()
            res = DNSresponse(dnsrequest)
            publicresponse = res.getpublicresponse()
            print("Publicrespons", publicresponse)
            ipaddress = res.getipaddress(publicresponse)
            dict = {"Answer": [{"data": ipaddress}]}
            return dict


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

    elif configtype == "upload":
        if request.method == 'POST':
            if "file" in request.files and "listtype" in request.form:
                file = request.files["file"]
                form = request.form
                print("form", form)
                if file.filename != "" and file.filename.split(".")[-1] in allowed_filetypes:
                    filename = secure_filename(file.filename)
                    savepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(savepath)
                    DNSconfig.setjson(form["listtype"] + "s", "add", savepath)

            elif "delete" in request.form:
                form = request.form
                deletepath = form["delete"].split(":")[1]
                DNSconfig.setjson(form["delete"].split(":")[0] + "s", "remove", deletepath)
                print(form["delete"].split(":")[0] + "s", "remove", deletepath)
                os.remove(deletepath)

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

    elif "getjson" in args:
        if request.method == 'POST':
            if "getjson" in args:
                dict = DNSconfig.getfromjson("all")
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
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #new socket has to be made every time, otherwise WINERROR:15004
    host = ''
    port = 53
    size = 512
    s.bind((host, port))

    data , addr = s.recvfrom(size)
    print("Raw request", data)

    res = DNSresponse(data)
    print("Domainname", res.domainname)

    ip, addresstype = DNSconfig.checkdomainname(res.domainname)
    print(ip, addresstype)

    if addresstype == "local":
        response = res.getlocalresponse(ip, 3600)

    elif addresstype == "public":
        response = res.getpublicresponse()

    print("Response", response)
    s.sendto(response, addr)
    s.close()
