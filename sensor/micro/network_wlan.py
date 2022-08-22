import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("gonewiththewind", "wangtao0303")
wlan.isconnected()



