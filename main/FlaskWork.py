import platform

from MyQR import myqr
import os
import webbrowser
from flask import Flask, render_template, send_from_directory, make_response

app = Flask(__name__)
import socket

ip = ""

import logging
import logging.handlers

LOG_FILE = 'tst.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger = logging.getLogger('tst')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def getSeparator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator


androidWorkDir = ""
workDir = "E:\\work\\statistics-android\\app\\build\\bakApk" + getSeparator()
filename = ""
rootPath = "F:\\Github\\JenkinsApk" + getSeparator()
port = "8090"


def getNewApk():
    files = os.listdir(workDir)
    print(files[-1])
    global androidWorkDir
    androidWorkDir = workDir + files[-1]
    lastDir = os.listdir(androidWorkDir)
    print(lastDir)
    for file in lastDir:  # 遍历文件夹
        logger.info(file)
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            if (file.endswith(".apk")):
                global filename
                filePath = androidWorkDir + getSeparator() + file
                logger.info(filePath)
                filename = file


@app.route('/download/link')
def download():
    logger.info("/download/link")
    getNewApk()
    logger.info("filename" + filename)
    # filename ="247.apk"
    # androidWorkDir ="F:\Github\JenkinsApk\main\static"
    # # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    response = make_response(send_from_directory(androidWorkDir, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response
    # return app.send_static_file(filename)
    # return send_from_directory(androidWorkDir, filename)


@app.route('/')
def index():
    print(getSeparator())

    picture_name = 'apk.png'

    return render_template('template.html', picture=picture_name, url="http://" + ip + ":" + port + "/download/link")


@app.route('/url')
def getDownloadUrl():
    return "http://" + ip + ":" + port + "/download/link"


@app.route('/picture/<picture>')
def serve_pictures(picture):
    return send_from_directory(rootPath + getSeparator() + 'picture', picture)


def generate_pic():
    save_dir = rootPath + 'picture'
    myqr.run(
        getDownloadUrl(),
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name='apk.png',
        save_dir=save_dir
    )
    logger.info('图片生成')


if __name__ == '__main__':
    ip = get_host_ip()
    generate_pic()
    getNewApk()
    logger.info('开始打开浏览器')

    logger.info(ip)
    webbrowser.open_new_tab("http://" + ip + ":" + port + "/")
    logger.info('打开浏览器')
    app.run(debug=False, host=ip, port=int(port), threaded=True)
