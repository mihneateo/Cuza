ooo
#!/usr/bin/env python3


import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import board
dir(board)
import busio
import gpiod
import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16, i2c=(busio.I2C(board.SCL, board.SDA)))
host_name = '192.168.1.118'  # IP Address of Raspberry Pi
host_port = 8000





def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" name="submit" value="shake">
               <input type="submit" name="submit" value="nod">
	       <input type="submit" name="submit" value="open">
               <input type="submit" name="submit" value="close">
               <input type="submit" name="submit" value="hands">
           </form>
           </body>
           </html>
        '''
        temp = getTemperature()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        

        if post_data == 'shake':
		print("shake")
		kit.servo[14].angle=80
		kit.servo[15].angle=80
		time.sleep(2)
		kit.servo[14].angle=90
		kit.servo[15].angle=90
		time.sleep(2)
		kit.servo[14].angle=100
		kit.servo[15].angle=100
		time.sleep(2)
		kit.servo[14].angle=90
		kit.servo[15].angle=90
	if post_data == 'nod':
		print("nod")
		kit.servo[12].angle=180
		time.sleep(1)
		kit.servo[12].angle=0
		time.sleep(1)
		kit.servo[10].angle=100
		time.sleep(1)
		kit.servo[10].angle=0
	if post_data == 'open':
		print("open") 
		kit.servo[11].angle=0
	if post_data == 'close':
		print("close")
		kit.servo[11].angle=180
	if post_data == 'hands':
		print("hands") 
		kit.servo[0].angle=80
		kit.servo[1].angle=80
		kit.servo[2].angle=80
		kit.servo[3].angle=80
		kit.servo[4].angle=80
		time.sleep(1)
		kit.servo[0].angle=90
		kit.servo[1].angle=90
		kit.servo[2].angle=90
		kit.servo[3].angle=90
		kit.servo[4].angle=90
		time.sleep(1)
		kit.servo[5].angle=80
		kit.servo[6].angle=80
		kit.servo[7].angle=80
		kit.servo[8].angle=80
		kit.servo[9].angle=80
		time.sleep(1)
		kit.servo[5].angle=90
		kit.servo[6].angle=90
		kit.servo[7].angle=90
		kit.servo[8].angle=90
		kit.servo[9].angle=90
		time.sleep(1)



        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
