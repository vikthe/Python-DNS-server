from DNS import DNSrequest
import socket
import configurations as config
config.init()

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
    ip, addresstype = req.checkdomainname()
    print(ip, addresstype)

    if addresstype == "local":
        response = req.getlocalresponse(ip, 3600)

    elif addresstype == "public":
        response = req.getpublicresponse()

    print("Response", response)
    s.sendto(response, addr)
