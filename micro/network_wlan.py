import network

wlan = network.WLAN(network.STA_IF)
wlan.connect("wifi_name", "wifi_password")
wlan.isconnected()
