import network
import time

SSID = '    '
PASSWORD = '    '
IP_ADDRESS = '    '

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        time.sleep(1)

    #ip = wlan.ifconfig()[0]
    
    wlan_status = wlan.ifconfig()
    wlan.ifconfig((IP_ADDRESS, wlan_status[1], wlan_status[2], wlan_status[3]))

    wlan_status = wlan.ifconfig()
    
    #return ip
    return wlan_status[0]


