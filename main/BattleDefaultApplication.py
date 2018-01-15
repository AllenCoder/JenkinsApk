from datetime import datetime

import os
from bottle import Bottle, run, request, response, static_file, abort
from json import dumps

app = Bottle()



# 静态文件
@app.route('/file')
def file():
    return static_file("170717007.xml", root="")


# 下载文件
@app.route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='', download=filename)


def openServer():
    run(app, host="10.0.31.14", port=8089)

# run(app, host="localhost", port=8089)
