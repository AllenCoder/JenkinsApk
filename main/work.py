from MyQR import myqr
import os

from bottle import route, run, template,static_file

@route('/download/link')
def downloan():
    return static_file('activity.apk',root="F:\Github\JenkinsApk\statics" , download=True)

@route('/')
def index():
    myqr.run(
        "http://workspace.devcoder.cn/wattforex.apk",
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name='apk.png',
        save_dir='F:\Github\JenkinsApk\picture'
    )
    url = "http://10.0.31.136:8098/download/link"
    src = "apk.png"

    picture_name = 'apk.png'
    return template('template', picture=picture_name)

@route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='F:\Github\JenkinsApk\picture')

run(host='10.0.31.136', port=8098)
