from machine import Pin
import network
import socket
import time

ssid = 'Nombtere de tu Wifi'
password = 'Contraseña de tu Wifi'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Conectando...")
    time.sleep(1)


print("Conectado. IP:", wlan.ifconfig()[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(0)

def get_response():
    action = "Apagar" if led.value() else "Encender"
    return f'''<!DOCTYPE html>
    <html>

    <head>
        <title>Encender Led</title>
    </head>

    <body>
        <h1>Encender Led</h1>
        <a href="/?led=toggle">{action}</a><br>
    </body>

    </html>
    '''

led = Pin(13, Pin.OUT)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1023)
    request_str = request.decode("utf-8")
    print(request_str)
    state = led.value()
    if "GET /?led=toggle" in request_str:
        led.value(not led.value())
    
    cl.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
    cl.send(get_response())
    cl.close()
