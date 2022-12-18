import json
from http.server import BaseHTTPRequestHandler, HTTPServer , HTTPStatus
import threading
import worker
import time

class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests

    count = 0

    def do_POST(self):
        datalen = int(self.headers['Content-Length'])
        data = self.rfile.read(datalen)
        self.obj = json.loads(data)
        f = open("client.json", "w")
        f.write(self.obj)
        f.close()
        myHandler.count += 1
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(json.dumps(myHandler.count).encode())
        myHandler.p = threading.Thread(target=worker.mymain)
        myHandler.p.start()


    def do_GET(self):
        request_path = self.path
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if request_path[0:4] == "/job":
            if myHandler.p.is_alive():
                message = {
                    "status": "your image is not ready"
                }
                self.wfile.write(json.dumps(message).encode())
            else:
                myHandler.url = "/media/image{}.jpg".format(myHandler.count)
                message = {"download url": myHandler.url}
                self.wfile.write(json.dumps(message).encode())
        elif request_path[0:6] == "/media":
            with open('image1.ps', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.wfile.write(json.dumps("bad request").encode())
        return


try:
    server = HTTPServer(('', 8877), myHandler)
    print('Started httpserver on port ', 8877)

    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
