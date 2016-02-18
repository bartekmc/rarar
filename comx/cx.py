
from bottle import route, run, template, static_file, redirect, hook, request
import os
import patoolib


STATIC_PREFIX = '/static'
STATIC_CACHE_PREFIX = '/cache'

APP_PATH = os.path.dirname(os.path.realpath(__file__))

templ = open(os.path.join(APP_PATH, 'tmpl.html')).read()

CACHE_PATH = os.path.join(os.path.abspath(APP_PATH), '.cx')
if not os.path.isdir(CACHE_PATH):
    os.makedirs(CACHE_PATH)


@route(STATIC_CACHE_PREFIX + '/<path:path>')
def staticfile_cache(path):
    return static_file(path, CACHE_PATH)


@route(STATIC_PREFIX + '/<path:path>')
def staticfile(path):
    return static_file(path, os.curdir)


@route('/f/<path:path>')
def open_file(path):
    path_cache = os.path.join(CACHE_PATH, path)
    path_file = os.path.join(os.path.abspath(os.curdir), path)
    if not os.path.isdir(path_cache):
        os.makedirs(path_cache)
        patoolib.extract_archive(path_file, outdir=path_cache)

    pages = []
    matches = []
    for root, dirnames, filenames in os.walk(path_cache):
        for filename in filenames:
                matches.append(os.path.relpath(os.path.join(root, filename),
                                               path_cache))

    files = sorted(matches)
    for f in files:
        p = os.path.join(os.sep, STATIC_CACHE_PREFIX, path, f)
        pages.append(p)

    if os.path.isfile(path_file):
        return template(templ, dirs=None, comics=None, pages=pages)

    return template("bbuug")


class Item:
    def __init__(self):
        self.name = None
        self.link = None
        self.directLink = None


@route('')
@route('/')
def redirect_to_root_path():
    return redirect('/r/')


@route('/r')
@route('/r/')
def root_path():
    return walk_path(os.curdir)


@route('/r/<path:path>')
@route('/r/<path:path>/')
def walk_path(path):
    print path
    files_dirs = next(os.walk(os.curdir + os.sep + path))
    filesx = files_dirs[2]
    dirsx = files_dirs[1]
    files = []
    dirs = []
    for f in filesx:

        if os.path.splitext(f)[1][0:3] != '.cb':
            continue

        i = Item()
        i.name = f
        i.link = os.path.join('/f/', path, f)
        i.directLink = os.path.join(STATIC_PREFIX, path, f)
        files.append(i)

    for d in dirsx:
        i = Item()
        i.name = d
        i.link = os.path.join('/r/', path, d)
        dirs.append(i)

    print(files)
    print(dirs)

    return template(templ, dirs=dirs, comics=files, pages=None)

run(host='127.0.0.1', port=8080)
