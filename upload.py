import time
import BDS
import urllib.parse
import json


class Upload:
    def __init__(self, boxnum):
        self.boxnum = boxnum
        self.setup()
    
    def setup(self):
        self.upload = BDS.Core()
        self.upload.at_return_command_off()
        self.upload.gnss_on()
        self.upload.net_on()
    
    def getloc(self):
        self.info = self.upload.refresh_gnss_info()
        self.data = {}
        self.data['latitude'] = str(self.upload.get_gnss_lat())
        self.data['longitude'] = str(self.upload.get_gnss_log())

    def uploaddata(self):
        self.getloc()
        self.data['box_number'] = self.boxnum
        self.data = json.dumps(self.data)
        self.data = urllib.parse.quote(self.data)
        self.res = self.upload.data_upload("fUz5dAK7VN", self.data)
        