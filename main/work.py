import platform

from MyQR import myqr
import os
import webbrowser
from bottle import route, run, template, static_file


def getSeparator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator


rootPath = "F:\Github\JenkinsApk" + getSeparator()
workDir = "E:\\work\\statistics-android\\app\\build\\bakApk" + getSeparator()
filePath = rootPath


def getNewApk():
    files = os.listdir(workDir)
    print(files[-1])
    path_files_ = workDir + files[-1]
    lastDir = os.listdir(path_files_)
    print(lastDir)
    for file in lastDir:  # 遍历文件夹
        print("-----", file)
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            if (file.endswith(".apk")):
                global filePath
                filePath = path_files_ + getSeparator() + file
                print("filePath === ", filePath)


@route('/download/link')
def download():
    return static_file(filePath, root="", download=True)


@route('/')
def index():
    print(getSeparator())
    myqr.run(
        filePath,
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name='apk.png',
        save_dir=rootPath + 'picture'
    )
    picture_name = 'apk.png'
    print('图片生成')
    return template('template', picture=picture_name)


@route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root=rootPath + 'picture')


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
    webbrowser.open_new_tab("http://localhost:8098/")
    print('打开浏览器')
    run(host='0.0.0.0', port=8098)
