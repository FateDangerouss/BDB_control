# -*- coding:utf-8 -*-
# python3环境下，需要先卸载serial模块，再重新安装pyserial模块，pyserial安装时有可能提示已安装，可以忽略
# 使用前命令行中运行如下代码
# 第一步
# pip3 uninstall serial
# 第二步
# pip3 install pyserial
import serial
import time


class Core:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyS0'
        self.ser.baudrate = 115200
        self.ser.open()
        self.ser.flushInput()

        self.rec_buff = ''
        self.upload_url = 'http://bds.teiit.com/api/Data/uploadText'
        self.download_url = 'http://bds.teiit.com/api/Data/download'
        self.gnss_info = {}
        self.gnss_data = ""
        self.timezone = +8

    # 发送AT指令通用方法
    def send_at(self, command, timeout=0.1):
        self.rec_buff = ''
        self.ser.write((command + '\r\n').encode())
        time.sleep(timeout)
        data = self.ser.read(self.ser.inWaiting())
        time.sleep(0.1)
        data = (data + self.ser.read(self.ser.inWaiting())).decode()
        if '\nERROR\r' in data:
            return 'AT COMMAND FAILED![' + command + ']'
        return data

    # 重启芯片
    def reset(self):
        self.send_at('AT+CRESET')

    # 关闭AT指令回显
    def at_return_command_off(self):
        self.send_at('ATE0')

    # 开启AT指令回显
    def at_return_command_on(self):
        self.send_at('ATE1')

    # 开启GNSS指示灯
    def gnss_led_on(self):
        self.send_at('AT+CLEDITST=1,1')

    # 关闭GNSS指示灯
    def gnss_led_off(self):
        self.send_at('AT+CLEDITST=0,0')

    # 开启GNSS
    def gnss_on(self):
        return self.send_at('AT+CGPS=1')

    # 关闭GNSS
    def gnss_off(self):
        self.gnss_led_off()
        return self.send_at('AT+CGPS=0')

    # 获取GNSS数据，并存在字典中
    def refresh_gnss_info(self):
        data = self.send_at('AT+CGNSSINFO').split("\r\n")
        self.gnss_info = {}
        arr = []
        for d in data:
            if len(d) > 10:
                self.gnss_data = d
                if d != "+CGNSSINFO: ,,,,,,,,,,,,,,,":
                    self.gnss_led_on()
                    arr = d[12:].split(",")
                    self.gnss_info["mode"] = arr[0]
                    self.gnss_info["GPS-SVs"] = int(arr[1])
                    self.gnss_info["GLONASS-SVs"] = int(arr[2])
                    self.gnss_info["BDS-SVs"] = int(arr[3])
                    self.gnss_info["lat"] = arr[4]
                    self.gnss_info["N/S"] = arr[5]
                    self.gnss_info["log"] = arr[6]
                    self.gnss_info["E/W"] = arr[7]
                    self.gnss_info["date"] = arr[8]
                    self.gnss_info["time"] = arr[9]
                    self.gnss_info["alt"] = arr[10]
                    self.gnss_info["speed"] = arr[11]
                    self.gnss_info["course"] = arr[12]
                    self.gnss_info["PDOP"] = arr[13]
                    self.gnss_info["HDOP"] = arr[14]
                    self.gnss_info["VDOP"] = arr[15]
                else:
                    self.gnss_led_off()
                return d

    # 获取UTC时间
    def get_time(self):
        data = self.gnss_info
        if data != {}:
            timeStr = str(self.gnss_info["date"]) + " " + str(self.gnss_info["time"])[:6]
            timeArray = time.strptime(timeStr, "%d%m%y %H%M%S")
            return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        else:
            return "NO SIGNAL"

    # 获取中国时间（+8区）
    def get_localtime(self, utctime):
        if utctime != "NO SIGNAL":
            import datetime
            return (datetime.datetime.strptime(utctime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
                hours=self.timezone)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return "NO SIGNAL"

    # 获取卫星数
    def get_svs(self):
        data = self.gnss_info
        gps = -1
        glonass = -1
        bds = -1
        if data != {}:
            bds = self.gnss_info["BDS-SVs"]
            gps = self.gnss_info["GPS-SVs"]
            glonass = self.gnss_info["GLONASS-SVs"]

        return {
            "BDS": bds,
            "GPS": gps,
            "GLONASS": glonass,
        }

    # 获取经纬度
    def get_location(self):
        data = self.gnss_info
        if data != {}:
            lat = float(self.gnss_info["lat"])
            log = float(self.gnss_info["log"])

            lat_d = int(lat / 100)
            log_d = int(log / 100)

            lat_m = (lat - lat_d * 100) / 60
            log_m = (log - log_d * 100) / 60

            lat = lat_d + lat_m
            log = log_d + log_m
        else:
            lat = -1
            log = -1

        return {
            "lat": lat,
            "log": log
        }

    # 获取纬度
    def get_gnss_lat(self):
        if self.gnss_info != {}:
            lat = float(self.gnss_info["lat"])

            lat_d = int(lat / 100)

            lat_m = int(lat - lat_d * 100)

            lat_s = round(((lat - lat_d * 100) - lat_m) * 60, 2)

            return str(lat_d) + "°" + str(lat_m) + "\'" + str(lat_s) + "\""
        else:
            return "-1°-1\'-1\""

    # 获取经度
    def get_gnss_log(self):
        if self.gnss_info != {}:
            log = float(self.gnss_info["log"])

            log_d = int(log / 100)

            log_m = int(log - log_d * 100)

            log_s = round(((log - log_d * 100) - log_m) * 60, 2)

            return str(log_d) + "°" + str(log_m) + "\'" + str(log_s) + "\""
        else:
            return "-1°-1\'-1\""

    # 获取高度
    def get_gnss_alt(self):
        if self.gnss_info != {}:
            return self.gnss_info['alt']
        else:
            return -99999

    # 获取高度
    def get_gnss_speed(self):
        if self.gnss_info != {}:
            return self.gnss_info['speed']
        else:
            return -1

    # 开启网络模式
    def net_on(self, apn="cmnet"):
        return self.send_at('AT+CGSOCKCONT=1,\"IP\",\"' + apn + '\"')

    # 获取http协议返回值
    def __net_http_get(self, url, wait=1):
        self.net_on('cmiot')
        self.send_at('AT+HTTPINIT')
        self.send_at('AT+HTTPPARA=\"URL\",\"' + url + '\"')
        res = self.send_at('AT+HTTPACTION=0', 3)
        temp_arr = res.split("\r\n")
        temp = temp_arr[3].split(",")
        data_range = temp[2]
        data = self.send_at('AT+HTTPREAD=0,' + str(data_range), wait)
        self.send_at('AT+HTTPTERM')
        return data

    # 上传数据，device_id=主机激活码，data=要上传的数据，remark=备注
    def data_upload(self, device_id, data, remark="", wait=3):
        i = 0
        url = self.upload_url + '/code/' + device_id + '/data/' + data + '/remark/' + remark
        while True:
            res = self.__net_http_get(url, wait)
            if res != '':
                temp = res.split('\r\n')
                return temp[4]
            i += 1
            if i == wait:
                return "timeout"

    # 上传数据，device_id=主机激活码，data=要上传的数据，remark=备注
    def data_download(self, device_id, remark="", count=1, wait=3):
        i = 0
        url = self.download_url + '/code/' + str(device_id) + '/count/' + str(count)
        if remark != "":
            url = url + '/remark/' + str(remark)
        print(url)
        while True:
            res = self.__net_http_get(url, wait)
            if res != '':
                temp = res.split('\r\n')
                return temp[4]
            i += 1
            if i == wait:
                return "timeout"

    # 输出日志
    def gnss_log(self, filename="log.txt"):
        fo = open(filename, "a+")
        fo.write(time.strftime("%Y-%m-%d %H:%M:%S:", time.localtime()) + str(self.gnss_data) + "\n")
        fo.close()
