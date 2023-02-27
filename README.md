# rcCar_AP

## 참고자료  

### AP모드 사용하기  
![image](https://user-images.githubusercontent.com/13882302/221561257-1103e8cb-5f72-4308-9816-ebce15410ca8.png)   

### Station 모드 개요도  
![image](https://user-images.githubusercontent.com/13882302/221561300-d1d471e0-43e7-4174-8e8b-676ee3da2545.png)

### Access Point 모드 개요도  
![image](https://user-images.githubusercontent.com/13882302/221561462-077cc0cd-9758-47a3-a247-4902d84121f7.png)

### 기본 AP모드 동작 확인 예제 코드
'''python
try:
 import usocket as socket        #importing socket
except:
 import socket
import network            #importing network
import gc
gc.collect()
ssid = 'RPI_PICO_AP'                  #Set access point name 
password = '12345678'      #Set your access point password


ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())
def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Welcome to microcontrollerslab!</h1></body></html>"""
  return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.bind(('', 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()
'''

[https://microcontrollerslab.com/raspberry-pi-pico-w-soft-access-point-web-server-example/](https://microcontrollerslab.com/raspberry-pi-pico-w-soft-access-point-web-server-example/)  
