import platform

from MyQR import myqr
import os
import webbrowser
from bottle import route, run, template, static_file
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


@route('/download/link')
def download():
    getNewApk()
    return static_file(filename, root=workDir, download=True)


@route('/')
def index():
    print(getSeparator())

    picture_name = 'apk.png'

    return template('templates', picture=picture_name, url="http://" + ip + ":"+port+"/download/link")


@route('/url')
def getDownloadUrl():
    return "http://" + ip + ":" + port + "/download/link"


@route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root=rootPath + getSeparator() + 'picture')


# 静态文件
@route('/file')
def file():
    return static_file("170717007.xml", root="")


# 下载文件
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='', download=filename)


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
    ip = "10.0.31.14"
    generate_pic()
    getNewApk()
    logger.info('开始打开浏览器')

    logger.info(ip)
    webbrowser.open_new_tab("http://" + ip + ":"+port+"/")
    logger.info('打开浏览器')
    run(host='0.0.0.0', port=port)
