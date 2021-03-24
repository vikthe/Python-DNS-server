import socket
import configurations as config

class DNSrequest:
    def __init__(self, requestdata):
        self.requestdata = requestdata
        self.domainname = ''
        self.stopbyte = ''

        length = ''
        length_byte = 12
        while length != 0:
            length = self.requestdata[length_byte]
            domainpart = self.requestdata[length_byte + 1:length_byte + length + 1]
            self.domainname += domainpart.decode("utf-8") + '.'
            length_byte = length_byte + length + 1

        self.stopbyte = length_byte - 1
        self.domainname = self.domainname[:-2]

    #forwardar DNS-paket från publik DNS
    def getpublicresponse(self):
        port = 53
        size = 512
        dnsarray = config.getfromjson("Public_DNS_servers")
        print(dnsarray)

        for address in dnsarray:
            try:
                server_address = (address, port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print(address)
                sock.sendto(self.requestdata, server_address)
                data, _ = sock.recvfrom(size)
            except:
                print(address + " fungerar ej, testar nästa publika DNS")

            sock.close()
            return data


    #skapar response från grunden
    def getlocalresponse(self, ipaddress, TTLinseconds):
        # Skapa DNS-header
        ID = self.requestdata[0:2]
        Flags = b'\x81\x80'
        QDCOUNT = b'\x00\x01'
        ANCOUNT = b'\x00\x01'
        NSCOUNT = b'\x00\x00'
        ARCOUNT = b'\x00\x00'
        Header = ID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

        # Skapa DNS-question
        QNAME = self.requestdata[12:self.stopbyte]
        QTYPE = b'\x00\x01'
        QCLASS = b'\x00\x01'
        Question = QNAME + b'\x00' + QTYPE + QCLASS

        # Skapa DNS-answer
        NAME = b'\xc0\x0c'
        TYPE = b'\x00\x01'
        CLASS = b'\x00\x01'

        try:
            TTL = TTLinseconds.to_bytes(4, byteorder='big')
        except OverflowError:
            print("OverflowError: TTL too large")
            packet = ID + b'\x81\x81'  # Format error
            return packet

        RDLENGTH = b'\x00\x04'

        RDATA = b''
        IParray = ipaddress.split(".")
        for part in IParray:
            try:
                RDATA += int(part).to_bytes(1, byteorder='big')
            except OverflowError:
                print("OverflowError: IP address has too large numbers")
                packet = ID + b'\x81\x81'  # Format error
                return packet

        Answer = NAME + TYPE + CLASS + TTL + RDLENGTH + RDATA

        #Lägger ihop alla delar till ett DNS-paket
        packet = Header + Question + Answer
        return packet


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




