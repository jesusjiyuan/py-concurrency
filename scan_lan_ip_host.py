# coding:utf-8

import time
import threading
import socket

threads = []

def get_hostname(ip):
    try:
        (name, aliaslist, addresslist) = socket.gethostbyaddr(ip)
        if name != ip:
            print(name ,'  ', ip)
                
    except Exception as e:
        return
    
      
def find_ip(ip_prefix):  
       
    for i in range(2,255):  
        ip = '%s.%s'%(ip_prefix,i)
        th=threading.Thread(target=get_hostname,args=(ip,))
        threads.append(th)
  
    
if __name__ == "__main__":  
    print ("start time",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    
    find_ip('192.168.30')
    for t in threads:
	    t.start()
    
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()   

    print ("end time",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))