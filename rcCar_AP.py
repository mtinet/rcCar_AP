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
s.listen(1)

# print('listening on', addr)
led.off()

#Template HTML
html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Zumo Robot Control</title>
            <center><H1>IoT Car</h1></center>
        </head>
        <body>
            <center>
                <form action="./forward">
                    <input type="submit" value="Forward" style="height:100px; width:100px; font-size:10px" />
                </form>
                <table>
                    <tr>
                        <td>
                            <form action="./left">
                                <input type="submit" value="Left" style="height:100px; width:100px; font-size:10px" />
                            </form>
                        </td>
                        <td>
                            <form action="./stop">
                                <input type="submit" value="Stop" style="height:100px; width:100px; font-size:10px" />
                            </form>
                        </td>
                        <td>
                            <form action="./right">
                                <input type="submit" value="Right" style="height:100px; width:100px; font-size:10px" />
                            </form>
                        </td>
                    </tr>
                </table>
                <form action="./back">
                    <input type="submit" value="Back" style="height:100px; width:100px; font-size:10px" />
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
