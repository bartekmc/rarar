from bottle import Bottle, route, run, template, static_file, redirect, hook, request
import shutil
import os
import patoolib


STATIC_PREFIX = '/static'
STATIC_CACHE_PREFIX = '/cache'

APP_PATH = os.path.dirname(os.path.realpath(__file__))

templ = open(os.path.join(APP_PATH, 'tmpl.html')).read()

CACHE_PATH = os.path.join(os.path.abspath(APP_PATH), '.cx')


class Item:
    def __init__(self):
        self.name = None
        self.link = None
        self.directLink = None


class ComicHost(Bottle):
    def __init__(self):
        super(ComicHost, self).__init__()

        self.cache_items = []
        self.clear_cache()

        self.route(STATIC_CACHE_PREFIX + '/<path:path>',
                   callback=self.staticfile_cache)
        self.route(STATIC_PREFIX + '/<path:path>', callback=self.staticfile)
        self.route('/f/<path:path>', callback=self.open_file)
        self.route('', callback=self.redirect_to_root_path)
        self.route('/', callback=self.redirect_to_root_path)
        self.route('/r', callback=self.root_path)
        self.route('/r/', callback=self.root_path)
        self.route('/r/<path:path>', callback=self.walk_path)
        self.route('/r/<path:path>/', callback=self.walk_path)

    def clear_cache(self):
        if os.path.isdir(CACHE_PATH):
            shutil.rmtree(CACHE_PATH)
        os.makedirs(CACHE_PATH)

    def trim_cache(self):
        if (len(self.cache_items) > 5):
            for c in self.cache_items[:2]:
                print "rmtree:", c
                shutil.rmtree(c)
            #self.cache_items = self.cache_items[:2]
            del self.cache_items[:2]

#    @route(STATIC_CACHE_PREFIX + '/<path:path>')
    def staticfile_cache(self, path):
        return static_file(path, CACHE_PATH)

#    @route(STATIC_PREFIX + '/<path:path>')
    def staticfile(self, path):
        return static_file(path, os.curdir)

#    @route('/f/<path:path>')
    def open_file(self, path):
        path_cache = os.path.join(CACHE_PATH, path)
        path_file = os.path.join(os.path.abspath(os.curdir), path)
        if not os.path.isdir(path_cache):
            os.makedirs(path_cache)
            patoolib.extract_archive(path_file, outdir=path_cache)
            self.cache_items.append(path_cache)
            self.trim_cache()

        pages = []
        matches = []
        for root, dirnames, filenames in os.walk(path_cache):
            for filename in filenames:
                    matches.append(os.path.relpath(os.path.join(root,
                                                                filename),
                                                   path_cache))

        files = sorted(matches)
        for f in files:
            p = os.path.join(os.sep, STATIC_CACHE_PREFIX, path, f)
            pages.append(p)

        back_link = os.path.join('/r/', os.path.split(path)[0])

        if os.path.isfile(path_file):
            return template(templ, dirs=None, comics=None, pages=pages,
                            back_link=back_link)

        return template("bbuug")

#    @route('')
#    @route('/')
    def redirect_to_root_path(self):
        return redirect('/r/')

#    @route('/r')
#    @route('/r/')
    def root_path(self):
        return self.walk_path(os.curdir)

#    @route('/r/<path:path>')
#    @route('/r/<path:path>/')
    def walk_path(self, path):
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
            i.link = os.path.join('/f/', path, f) + "#2"
            i.directLink = os.path.join(STATIC_PREFIX, path, f)
            files.append(i)

        for d in dirsx:
            i = Item()
            i.name = d
            i.link = os.path.join('/r/', path, d)
            dirs.append(i)

        i = Item()
        i.name = "COFNIJ"
        i.link = os.path.join('/r/', os.path.split(path)[0])
        if len(dirs) > 0:
            dirs.insert(0, i)
        else:
            files.insert(0, i)

        print(files)
        print(dirs)

        return template(templ, dirs=dirs, comics=files, pages=None)


comicHost = ComicHost()
comicHost.run(host='192.168.1.105', port=8080)


