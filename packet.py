import re

class Packet:
    regex='Frame [0-9]+:'
    frame_num = 'Frame ([0-9]+):'

    def __init__(self,packet):
        self.packet = packet
        self.http=Http(packet)

    def frame_number(self):
        m = re.search(Packet.frame_num,self.packet)   
        if m != None:
            return int(m.group(1))

class Http:
    regex = 'Hypertext Transfer Protocol'
    data='Line-based text data: (.*)'
    request_uri='Request URI: ((/[\._&%$a-zA-Z0-9]+)+)'
    status_code='Status Code: ([0-9]+)'

    def __init__(self,packet):
        self.packet = packet
    def get_request_uri(self):
        m = re.search(Http.request_uri,self.packet)
        if m != None:
            return m.group(1)
        else:
            return None
    def get_status_code(self):
        m = re.search(Http.status_code,self.packet)
        if m != None:
            return int(m.group(1))
        else:
            return None
    def get_data(self):
        m = re.search(Http.data,self.packet,re.DOTALL)
        if m != None:
            return m.group(1)
        else:
            return None
