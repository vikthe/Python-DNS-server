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

    #forwardars DNS-request to public DNS
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


    #create response from scratch
    def getlocalresponse(self, ipaddress, TTLinseconds):
        # Create DNS-header
        ID = self.requestdata[0:2]
        Flags = b'\x81\x80'
        QDCOUNT = b'\x00\x01'
        ANCOUNT = b'\x00\x01'
        NSCOUNT = b'\x00\x00'
        ARCOUNT = b'\x00\x00'
        Header = ID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

        # create DNS-question
        QNAME = self.requestdata[12:self.stopbyte]
        QTYPE = b'\x00\x01'
        QCLASS = b'\x00\x01'
        Question = QNAME + b'\x00' + QTYPE + QCLASS

        # create DNS-answer
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

        #adds all parts to the packet
        packet = Header + Question + Answer
        return packet