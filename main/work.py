import platform

from MyQR import myqr
import os

from bottle import route, run, template,static_file
def getSeparator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator
rootPath =os.path.dirname(os.getcwd())+getSeparator()
@route('/download/link')
def download():
    return static_file('activity.apk',root=rootPath+"static" , download=True)

@route('/')
def index():
    myqr.run(
        "https://o6bw6tmdt.qnssl.com/app-release.apk",
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name='apk.png',
        save_dir=rootPath+'picture'
    )
    picture_name = 'apk.png'
    return template('template', picture=picture_name)

@route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root=rootPath+'picture')

run(host='10.0.31.136', port=8098)
