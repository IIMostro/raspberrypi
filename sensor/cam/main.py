import time

import camera
import network
import usocket as socket


def connection_wifi():
    ssid = 'gonewiththewind'
    password = 'wangtao0303'

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass
    print('Connection successful')
    print(station.ifconfig())

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    on = request.find('/capture')
    camera.init(0)
    while True:
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: image/jpg\n')
      conn.send('Connection: close\n\n')
      buf = camera.capture()
      conn.sendall(buf)
      time.sleep(1)

server()
