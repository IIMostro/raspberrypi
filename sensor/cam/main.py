import usocket as socket
import network
import esp
import camera
import gc


esp.osdebug(None)
gc.collect()

ssid = 'gonewiththewind'
password = 'wangtao0303'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass
print('Connection successful')
print(station.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  on = request.find('/capture')
  if on == 6:
      camera.init()
      buf = camera.capture()
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: image/jpg\n')
      conn.send('Connection: close\n\n')
      conn.sendall(buf)
      camera.deinit()
      conn.close()
  else:
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: text/html\n')
      conn.send('Connection: close\n\n')
      conn.sendall("hello")
      conn.close()