from bottle import Bottle, route, run, template, static_file, redirect, hook, request
import shutil
import os
#import patoolib
import urllib

import threading
import PIL
from PIL import Image
import rarfile

from operator import itemgetter, attrgetter, methodcaller

rarfile.PATH_SEP = '/'




def resize(im, percent):
    """ retaille suivant un pourcentage 'percent' """
    w, h = im.size
    return im.resize(((percent*w)/100, (percent*h)/100))
def resize2(im, pixels):
    """ retaille e le plus long en 'pixels' 
        (pour tenir dans une frame de pixels x pixels)
    """
    (wx, wy) = im.size
    rx = 1.0*wx/pixels
    ry = 1.0*wy/pixels
    if rx > ry:
        rr = rx
    else:
        rr = ry
    return im.resize((int(wx/rr), int(wy/rr)))

class Unpack:
    def __init__(self, archive_path_file, out_dir, page=0):
        self.archive = archive_path_file
        self.page = page
        self.out_dir = out_dir

    def unpack(self, obsr=None):
        rar = rarfile.RarFile(self.archive)
        rfiles = rar.infolist()
        rfiles = sorted(rfiles, key=attrgetter('filename'))
        rfiles = rfiles[self.page:] + rfiles[:self.page]
        for i in rfiles:
            rar.extract(i, self.out_dir)
            #im = Image.open(os.path.join(self.out_dir, i.filename))
            print os.path.join(self.out_dir, i.filename)
            ff = os.path.relpath(os.path.join(self.out_dir, i.filename))
            im = Image.open(ff)
            im = resize(im, 70)
            r = os.path.split(ff) 
            im.save(os.path.join(r[0], "bmc_"+r[1]))
            print "resize:", os.path.join(self.out_dir, i.filename)

#threads = []
#for i in range(5):
#    t = threading.Thread(target=worker)
#    threads.append(t)
#    t.start()

STATIC_PREFIX = '/static'
STATIC_CACHE_PREFIX = '/cache'

APP_PATH = os.path.dirname(os.path.realpath(__file__))

templ = open(os.path.join(APP_PATH, 'tmpl.html')).read()

CACHE_PATH = os.path.join(os.path.abspath(APP_PATH), '.cx')

DB_PATH = os.path.join(os.path.abspath(APP_PATH), '.db')

DB_FILE = os.path.join(DB_PATH, 'db.file')

if not os.path.isdir(DB_PATH):
    os.makedirs(DB_PATH)
    fdb = open(DB_FILE, 'w+')


class Item:
    def __init__(self):
        self.name = None
        self.link = None
        self.directLink = None
        self.read_icon = False
        self.finished_icon = False


class HtmlObj:
    def __init__(self):
        self.pages = None
        self.dirs = None
        self.comics = None
        self.back_link = None
        self.image_src = None
        self.saveX_link = ""
        self.last_page = "2"
        self.prev_page = "2"
        self.cur_page = "2"
        self.next_page = "2"
        self.folder_back = None


class ComicHost(Bottle):
    def __init__(self):
        super(ComicHost, self).__init__()

        self.cache_items = []
        self.clear_cache()

        self.route(STATIC_CACHE_PREFIX + '/<path:path>',
                   callback=self.staticfile_cache)
        self.route(STATIC_PREFIX + '/<path:path>', callback=self.staticfile)
        self.route('/f/<path:path>/page/<page:int>', callback=self.open_file_a)
        self.route('/f/<path:path>', callback=self.open_file)
        self.route('', callback=self.redirect_to_root_path)
        self.route('/', callback=self.redirect_to_root_path)
        self.route('/r', callback=self.root_path)
        self.route('/r/', callback=self.root_path)
        self.route('/r/<path:path>', callback=self.walk_path)
        self.route('/r/<path:path>/', callback=self.walk_path)

        self.route('/s/r/<path:path>/<page:int>', callback=self.saveX)

    def saveX(self, path, page):
        print "SAVEX:", path, page
        path = urllib.unquote(path)
        f = open(DB_FILE, 'r+')
        flines = f.readlines()
        #print flines
        fout = []
        needAdd = True 
        for l in flines:
            if path in l:
                needAdd = False
                fout.append(path + ',' + str(page))
            else:
                if l != '\n':
                    fout.append(l.strip())

        if needAdd:
            fout.append(path + ',' + str(page))
        
        print repr("write:"+ '\n'.join(fout))
        f.seek(0)
        f.truncate()
        f.write('\n'.join(fout))
        f.close()
        
        return template("{{X}} {{P}}", X=path, P=page)

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
        resize = request.query.resize
        print "staticfile_cache:", path, resize
        return static_file(path, CACHE_PATH)

#    @route(STATIC_PREFIX + '/<path:path>')
    def staticfile(self, path):
        resize = request.query.resize
        print "staticfile:", path, resize
        return static_file(path, os.curdir)

    def unpack(self, path_file, path_cache, page=0):
        """thread worker function"""
        print 'Unpack:', path_file, path_cache 

        #patoolib.extract_archive(path_file, outdir=path_cache)
        u = Unpack(path_file, path_cache, page)
        u.unpack()

        self.cache_items.append(path_cache)
        self.trim_cache()

#        for root, dirnames, filenames in os.walk(path_cache):
#            for filename in filenames:
#                    ff = os.path.relpath(os.path.join(root, filename))
#                    im = Image.open(ff)
#                    im = resize(im, 70)
#                    r = os.path.split(ff) 
#                    im.save(os.path.join(r[0], "bmc_"+r[1]))
#                    print "resize:", os.path.relpath(os.path.join(root, filename))

        return



    def open_file_a(self, path, page):
        hobj = HtmlObj()

        path_cache = os.path.join(CACHE_PATH, path)
        path_file = os.path.join(os.path.abspath(os.curdir), path)
        pages = []
        matches = []

        if not os.path.isdir(path_cache):
            os.makedirs(path_cache)

#            print repr(patoolib.list_archive(path_file))

            rf = rarfile.RarFile(path_file)
            xxfiles = rf.namelist()

            xpage = page
            if xpage ==999:
                xpage = len(xxfiles)-1
            t = threading.Thread(target=self.unpack, args=(path_file, path_cache, xpage))
            t.start()


            for f in xxfiles:
                if "bmc_" not in f:
                    matches.append(f)

        else:

            rf = rarfile.RarFile(path_file)
            xxfiles = rf.namelist()
            for f in xxfiles:
                matches.append(f)

        files = sorted(matches)
        x = int(1)
        for f in files:
            p = os.path.join(os.sep, 'f/', path, 'page', str(x))
            pages.append(p)
            x+=1

        back_link = os.path.join('/r/', os.path.split(path)[0])

        if page ==999:
            page = len(files)-1
        hobj.dirs = None
        hobj.comics = None
        #hobj.image_src = os.path.join(os.sep, STATIC_CACHE_PREFIX, path, files[page])
	fx = files[page]
	fx = fx.replace('\\','/')
	print "fx1", fx
        fx = os.path.split(fx)
	print "fx2", fx
        fx = os.path.join(fx[0], "bmc_"+fx[1])
	print "fx3", fx
        hobj.image_src = os.path.join(os.sep, STATIC_CACHE_PREFIX, path, fx)
        #hobj.image_src = os.path.join(os.sep, STATIC_CACHE_PREFIX, path, "bmc_"+files[page])

        hobj.pages = pages
        hobj.prev_page = pages[page-2] 
        hobj.cur_page = pages[page-1] 
        hobj.next_page = pages[page]
        hobj.last_page = '2' 
        hobj.back_link = back_link

        f = open(DB_FILE, 'r')
        flines = f.readlines()
        for l in flines:
            if path in l:
                hobj.last_page = int(l.split(',')[1])
        f.close()

        x = os.path.join('/s/r/', path)
        hobj.saveX_link = urllib.quote(x)
        print "ZZZZ", len(pages), page
        if (page >= len(pages)):
            self.saveX(hobj.saveX_link, 999)
        else:
            self.saveX(hobj.saveX_link, page)
        
        if os.path.isfile(path_file):
            return template(templ, hobj=hobj)

        return template("bbuug")

#    @route('/f/<path:path>')
    def open_file(self, path):
        pass
        return
#        return self.open_file_a(path, 0)

        hobj = HtmlObj()
        path_cache = os.path.join(CACHE_PATH, path)
        path_file = os.path.join(os.path.abspath(os.curdir), path)
        if not os.path.isdir(path_cache):
            os.makedirs(path_cache)

            t = threading.Thread(target=self.unpack, args=(path_file, path_cache))
#            threads.append(t)
            t.start()

#            patoolib.extract_archive(path_file, outdir=path_cache)
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

        hobj.dirs = None
        hobj.comics = None
        hobj.pages = pages
        hobj.prev_page = "1"
        hobj.cur_page = pages[0] 
        hobj.next_page = pages[1]
        hobj.last_page = '2' 
        hobj.back_link = back_link

        f = open(DB_FILE, 'r')
        flines = f.readlines()
        for l in flines:
            #print path, l
            if path in l:
                hobj.last_page = int(l.split(',')[1])
        f.close()

        x = os.path.join('/s/r/', path)
        hobj.saveX_link = urllib.quote(x)
        if os.path.isfile(path_file):
            return template(templ, hobj=hobj)

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
        hobj = HtmlObj()
        print path
        files_dirs = next(os.walk(os.curdir + os.sep + path))
        filesx = sorted(files_dirs[2])
        dirsx = sorted(files_dirs[1])
        files = []
        dirs = []
        for f in filesx:

            if os.path.splitext(f)[1][0:3] != '.cb':
                continue

            i = Item()
            i.name = f
            i.link = os.path.join('/f/', path, f, 'page', str(1))
            i.directLink = os.path.join(STATIC_PREFIX, path, f )
            files.append(i)

            fo = open(DB_FILE, 'r')
            flines = fo.readlines()
            #print path, f
            last_page = 1
            for lz in flines:
                if os.path.join(path, f) in lz:
                    last_page = int(lz.split(',')[1])
            fo.close()
            if last_page == 999:
                i.finished_icon = True 
            if last_page > 1 and last_page != 999:
                i.read_icon = True

            i.link = os.path.join('/f/', path, f, 'page', str(last_page))

        for d in dirsx:
            i = Item()
            i.name = d
            i.link = os.path.join('/r/', path, d)
            dirs.append(i)

#        i = Item()
#        i.name = "COFNIJ"
#        i.link = os.path.join('/r/', os.path.split(path)[0])
#        if len(dirs) > 0:
#            dirs.insert(0, i)
#        else:
#            files.insert(0, i)

        hobj.folder_back = os.path.join('/r/', os.path.split(path)[0])
        hobj.dirs = dirs
        hobj.comics = files
        hobj.pagers = None
        return template(templ, hobj=hobj)


comicHost = ComicHost()
comicHost.run(host='0.0.0.0', port=8080, reloader=True)


