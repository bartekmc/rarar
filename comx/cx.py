
from bottle import route, run, template, static_file, redirect
import os
import patoolib

def p(var):
    for k, v in list(locals().iteritems()):
         if v is var:
             print "%s:%s" % (k , v)
             return
    print '?'

templ = "{{files}}"

CACHE_PATH = os.path.join(os.path.abspath(os.curdir), '.cx')
if not os.path.isdir(CACHE_PATH):
    os.makedirs(CACHE_PATH)

@route('/f/<path:path>')
def open_file(path):
    path_cache = os.path.join(CACHE_PATH, path)
    path_file = os.path.join(os.path.abspath(os.curdir), path)
    if not os.path.isdir(path_cache):
        os.makedirs(path_cache)
        patoolib.extract_archive(path_file, outdir=path_cache)

    files = os.listdir(path_cache)

    if os.path.isfile(path_file):
        return template("{{filename}}<br\>{{path_cache}}<br/>{{files}}",files=files, filename=path_file, path_cache=path_cache)
    return template("bbuug")


@route('/r/<path:path>')
def path_walk(path):
    print path
    files_dirs = next(os.walk(os.curdir + os.sep + path))
    files = files_dirs[2]
    dirs = files_dirs[1]
    print(files)
    print(dirs)

#    itemsd = sorted(itemsd)
#    itemsf = sorted(itemsf)
#    iii = []
#    dirsc = 0
#    print '3'
#    if index == 0:
#        for i in itemsd:
#            print '3.'
#            it = Item()
#            it.navi = navi
#            it.path = os.curdir + os.sep + path + i
#            it.isDirx = True
#            #if it.isDir() and index == 0:
#            #    dirsc=dirsc+1
#            if it.dirName() == select:
#                it.isActive = True
#
#            #if (int(index) == 0 and it.isDir()) or not it.isDir():
#            iii.append(it)
#
#    for i in itemsf[index:index+count]:
#        it = Item()
#        it.path = os.curdir + os.sep + path + i
#            
#        #if it.isDir() and index == 0:
#        #    dirsc=dirsc+1
#        #if it.dirName() == select:
#        #    it.isActive = True
#
#        #if (int(index) == 0 and it.isDir()) or not it.isDir():
#        iii.append(it)
#
#    if len(itemsf[index:index+count]) > 0:
#        if direction == 'up':
#            iii[-1].isActive = True
#        elif direction == 'down':
#            iii[0].isActive = True
#
#    print '4a'
#        #iii = sorted(iii)
#    print '4b'
#    for x in iii:
#        print x
#
#    print index, index+dirsc+count
    return template(templ, files=files)

run(host='127.0.0.1', port=8080)
