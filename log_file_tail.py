# -*- coding:utf-8 -*-

import os
import time
from flask import Flask, send_from_directory
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)


@app.route("/home")
def page():
    return send_from_directory("./", "log_tail.html")



@sockets.route("/log_tail")
def log_tail(ws):
    while not ws.closed:
        log_file = ws.receive()
        if not os.path.exists(log_file):
            ws.send("{}can not find the file！！！".format(log_file))
        while os.path.exists(log_file):
            fsize = os.path.getsize(log_file)
            fsize_mb = round(fsize/float(1024*1024), 2)
            ws.send("file size: {}MB".format(fsize_mb))
            if fsize_mb > 100:
                ws.send("the file is too big,go and fix it。。。")
            ws.send("######start log file monitoring######")

            number = 0
            position = 0
            with open(log_file, mode="r") as f:
                f.seek(fsize)
                while True:
                    line = f.readline().strip()
                    if line:
                        number += 1
                        ws.send("[{}] {}".format(number, line))

                    cur_position = f.tell()
                    if cur_position == position:
                        time.sleep(0.1)
                        continue
                    else:
                        position = cur_position


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(("0.0.0.0", 30066), app, handler_class=WebSocketHandler)
    print("web server start ...")
    server.serve_forever()
