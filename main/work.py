import platform

from MyQR import myqr
import os
import webbrowser
from bottle import route, run, template, static_file
import socket

ip =""

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

androidWorkDir =""
workDir = "E:\\work\\statistics-android\\app\\build\\bakApk" + getSeparator()
filename =""
rootPath ="F:\\Github\\JenkinsApk"+getSeparator()
def getNewApk():
    files = os.listdir(workDir)
    print(files[-1])
    global  androidWorkDir
    androidWorkDir = workDir + files[-1]
    lastDir = os.listdir(androidWorkDir)
    print(lastDir)
    for file in lastDir:  # 遍历文件夹
        print("-----", file)
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            if (file.endswith(".apk")):
                global filename
                filePath = androidWorkDir + getSeparator() + file
                print("filePath === ", filePath)
                filename =file

@route('/download/link')
def download():
    getNewApk()
    return static_file(filename, root=androidWorkDir, download=True)


@route('/')
def index():
    print(getSeparator())

    save_dir =rootPath+ 'picture'

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
    picture_name = 'apk.png'
    print('图片生成')
    return template('template', picture=picture_name)

@route('/url')
def getDownloadUrl():
    return "http://" + ip + ":8098/download/link"


@route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root=rootPath+getSeparator() + 'picture')


# 静态文件
@route('/file')
def file():
    return static_file("170717007.xml", root="")


# 下载文件
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='', download=filename)


if __name__ == '__main__':
    getNewApk()
    print('开始打开浏览器')
    ip = get_host_ip()
    print(ip)
    webbrowser.open_new_tab("http://"+ip+":8098/")
    print('打开浏览器')
    run(host=ip, port=8098)
