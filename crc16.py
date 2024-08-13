def crc16(text):
    """
 
    hj 212-2017 crc16效验
 
    :param text: 待效验的字符串
 
    :return: result
 
    """
 
    data = bytearray(text, encoding='utf-8')
 
    crc = 0xffff
 
    dxs = 0xa001
 
    for i in range(len(data)):
 
        hibyte = crc >> 8
 
        crc = hibyte ^ data[i]
 
        for j in range(8):
 
            sbit = crc & 0x0001
 
            crc = crc >> 1
 
            if sbit == 1:
                crc ^= dxs
 
    return hex(crc)[2:]
 
 
if __name__ == '__main__':
    result = crc16('QN=20191015160812988;ST=22;CN=2011;PW=111111;MN=18092222;Flag=5;CP=&&DataTime=20191015160812;a34004-Rtd=15.5;a34002-Rtd=21.7;LA-Rtd=55.4;a01001-Rtd=0.0;a01002-Rtd=0.0;a01007-Rtd=0.0;a01008-Rtd=0;a34001-Rtd=0.0&&')
    result = crc16('QN=20160801085857223;ST=32;CN=1062;PW=100000;MN=010000A8900016F000169DC0;Flag=5;CP=&&RtdInterval=30&&')
    print(result)