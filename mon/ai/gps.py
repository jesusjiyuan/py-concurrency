import math
from loguru import logger
# import serial
# from time import sleep
# s = serial.Serial('/dev/COM4', 9600)
#
# while True:
#     received_data = s.read(s.in_waiting)
#     if not received_data == "":
#         print(received_data.decode("ascii",'ignore'))
#     sleep(1)

import serial
import time


# 配置日志保存到文件
logger.add("gps-app.log", rotation="300MB")

def start():
    # 设置串口号，例如 COM3，Linux下可能是 /dev/ttyUSB0
    port = 'COM4'
    baudrate = 9600

    # 打开串口
    ser = serial.Serial(port, baudrate, timeout=1)

    try:
        while True:
            if ser.in_waiting > 0:
                incoming_data = ser.readline().decode('ascii').rstrip()  # 读取一行数据并解码
                print(incoming_data)  # 打印数据
                # 在这里可以添加解析GPS数据的代码
    except KeyboardInterrupt:
        print("程序被用户中断")

    finally:
        ser.close()  # 关闭串口连接

import re

def parse_gngga(gps_data):
    # 定义 GNGGA 语句的正则表达式模式
    pattern = re.compile(r'\$GNGGA,(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*)\*([0-9A-F]{2})')

    match = pattern.match(gps_data)
    if match:
        time = match.group(1)
        latitude = match.group(2)
        latitude_direction = match.group(3)
        longitude = match.group(4)
        longitude_direction = match.group(5)
        fix_quality = int(match.group(6))
        num_satellites = int(match.group(7))
        hdop = float(match.group(8))
        altitude = float(match.group(9))
        altitude_unit = match.group(10)
        geoid_separation = float(match.group(11))
        geoid_separation_unit = match.group(12)
        age_of_differential_corrections = match.group(13)
        differential_reference_station_id = match.group(14)
        #checksum = match.group(15)

        print(f"Time: {time}")
        print(f"Latitude: {latitude} {latitude_direction}")
        print(f"Longitude: {longitude} {longitude_direction}")
        print(f"Fix Quality: {fix_quality}")
        print(f"Number of Satellites: {num_satellites}")
        print(f"HDOP: {hdop}")
        print(f"Altitude: {altitude} {altitude_unit}")
        print(f"Geoid Separation: {geoid_separation} {geoid_separation_unit}")
        print(f"Age of Differential Corrections: {age_of_differential_corrections}")
        print(f"Differential Reference Station ID: {differential_reference_station_id}")
        #print(f"Checksum: {checksum}")
        # lat = math.floor(float(latitude))/60
        # lon = math.floor(float(longitude))/60
        lat = float(latitude)/60
        lon = float(longitude)/60
        print(f"lat:{lat} ,lon:{lon}",)
        p = [math.floor(float(longitude)/100),math.floor(float(latitude)/100)]
        p = [p[0]+(float(longitude) - p[0]* 100)/60,p[1]+(float(latitude) - p[1] *100)/60]
        print(f"p: {p}")
    else:
        print("Invalid GNGGA data")


def bd():
    from pyproj import Transformer

    def bd09_to_wgs84(bd_lon, bd_lat):
        transformer = Transformer.from_crs("BD09", "WGS84")
        wgs84_lon, wgs84_lat = transformer.transform(bd_lon, bd_lat)
        return wgs84_lon, wgs84_lat
    # 示例：百度地图坐标
    bd_lon = 120.123456
    bd_lat = 30.123456
    wgs84_lon, wgs84_lat = bd09_to_wgs84(bd_lon, bd_lat)
    print(f"WGS84 经度: {wgs84_lon}, WGS84 纬度: {wgs84_lat}")


# gps_data = "$GNGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
#gps_data = "$GNGGA,071826.000,3115.46124,N,12129.08821,E,1,25,0.6,7.5,M,11.2,M,,*40"
gps_data = "$GNGGA,071642.000,3115.45806,N,12129.08764,E,1,10,1.1,-11.0,M,11.2,M,,*57"
parse_gngga(gps_data)

# 接收数据
#start()


import serial.tools.list_ports
[print(i) for i in serial.tools.list_ports.comports()]