from scapy.all import srp, Ether, ARP  
IpScan = '192.168.30.1/255'  
try:  
    ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=IpScan), timeout=2)  
except Exception as e:  
    print(e)  
else:  
    for send, rcv in ans:  
        ListMACAddr = rcv.sprintf("%Ether.src%---%ARP.psrc%")  
        print(ListMACAddr)