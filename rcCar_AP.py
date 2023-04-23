import socket
import network
import machine

# 접속을 위한 ssid, password 설정 
ssid = 'rcCar_AP'
password = '123456789'

led = machine.Pin("LED",machine.Pin.OUT)


# AP모드 설정
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
  pass

print('Ready to Connection')
print("Connect to the WiFi with the '" + ssid + "'")
print("Connection IP: " + ap.ifconfig()[0])
print()

# 소켓 접속을 위한 설정
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1) # AP 접속자 수를 1명으로 제한함 

# print('listening on', addr)
led.off()

#Template HTML
html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>IoT RC Car</title>
        <center><H1>IoT RC Car</h1></center>
        <style>
          /* 버튼 디자인 */
          .button {{
            border: none;
            color: white;
            padding: 16px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
            background-color: #4CAF50;
            width: 120px;
            height: 60px;
            border-radius: 20%;
            box-shadow: 2px 2px 2px #888888;
          }}
          .button:hover {{
            background-color: #3e8e41;
          }}
        </style>

      </head>
      <body>
        <center>
          <form action="./forward">
            <button class="button" type="submit">Forward</button>
          </form>
          <br>
          <table>
            <tr>
              <td>
                <form action="./left">
                  <button class="button" type="submit">Left</button>
                </form>
              </td>
              <td>
                <form action="./stop">
                  <button class="button" type="submit">Stop</button>
                </form>
              </td>
              <td>
                <form action="./right">
                  <button class="button" type="submit">Right</button>
                </form>
              </td>
            </tr>
          </table>
          <br>
          <form action="./back">
            <button class="button" type="submit">Back</button>
          </form>
        </center>
      </body>
    </html>
"""


# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        # print('client connected from', addr)
        
        request = cl.recv(1024)
        led.on()
        # print(request)
        
        if b'GET /forward' in request:
            # forward 동작 수행
            print("Input Command: forward")
        elif b'GET /left' in request:
            # left 동작 수행
            print("Input Command: left")
        elif b'GET /right' in request:
            # right 동작 수행
            print("Input Command: right")
        elif b'GET /stop' in request:
            # stop 동작 수행
            print("Input Command: stop")
        elif b'GET /back' in request:
            # back 동작 수행
            print("Input Command: back")
            
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        led.off()

    except OSError as e:
        cl.close()
        print('connection closed')



