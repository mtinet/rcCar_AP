import socket
import network
import machine

ssid = 'rcCar_AP'
password = '123456789'

led = machine.Pin("LED",machine.Pin.OUT)

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

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

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)
led.off()

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        led.on()
        print(request)

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        led.off()

    except OSError as e:
        cl.close()
        print('connection closed')
