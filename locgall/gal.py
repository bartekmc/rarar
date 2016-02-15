from bottle import route, run, template, static_file, redirect
import os

templ = """
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>fullPage.js One Page Scroll Sites</title>
    <meta name="author" content="Alvaro Trigo Lopez" />
    <meta name="description" content="fullPage plugin by Alvaro Trigo. Create fullscreen pages fast and simple. One page scroll like iPhone website." />
    <meta name="keywords"  content="fullpage,jquery,alvaro,trigo,plugin,fullscren,screen,full,iphone5,apple" />
    <meta name="Resource-type" content="Document" />
 
<script src="http://code.jquery.com/jquery-latest.min.js"></script> 

<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/fullPage.js/2.7.7/jquery.fullPage.css" />

<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/fullPage.js/2.7.7/jquery.fullPage.js"></script>

<style>

.sk-circle {
  margin: 100px auto;
  width: 140px;
  height: 140px;
  position: relative;
}
.sk-circle .sk-child {
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
}
.sk-circle .sk-child:before {
  content: '';
  display: block;
  margin: 0 auto;
  width: 15%;
  height: 15%;
  background-color: #333;
  border-radius: 100%;
  -webkit-animation: sk-circleBounceDelay 1.2s infinite ease-in-out both;
          animation: sk-circleBounceDelay 1.2s infinite ease-in-out both;
}
.sk-circle .sk-circle2 {
  -webkit-transform: rotate(30deg);
      -ms-transform: rotate(30deg);
          transform: rotate(30deg); }
.sk-circle .sk-circle3 {
  -webkit-transform: rotate(60deg);
      -ms-transform: rotate(60deg);
          transform: rotate(60deg); }
.sk-circle .sk-circle4 {
  -webkit-transform: rotate(90deg);
      -ms-transform: rotate(90deg);
          transform: rotate(90deg); }
.sk-circle .sk-circle5 {
  -webkit-transform: rotate(120deg);
      -ms-transform: rotate(120deg);
          transform: rotate(120deg); }
.sk-circle .sk-circle6 {
  -webkit-transform: rotate(150deg);
      -ms-transform: rotate(150deg);
          transform: rotate(150deg); }
.sk-circle .sk-circle7 {
  -webkit-transform: rotate(180deg);
      -ms-transform: rotate(180deg);
          transform: rotate(180deg); }
.sk-circle .sk-circle8 {
  -webkit-transform: rotate(210deg);
      -ms-transform: rotate(210deg);
          transform: rotate(210deg); }
.sk-circle .sk-circle9 {
  -webkit-transform: rotate(240deg);
      -ms-transform: rotate(240deg);
          transform: rotate(240deg); }
.sk-circle .sk-circle10 {
  -webkit-transform: rotate(270deg);
      -ms-transform: rotate(270deg);
          transform: rotate(270deg); }
.sk-circle .sk-circle11 {
  -webkit-transform: rotate(300deg);
      -ms-transform: rotate(300deg);
          transform: rotate(300deg); }
.sk-circle .sk-circle12 {
  -webkit-transform: rotate(330deg);
      -ms-transform: rotate(330deg);
          transform: rotate(330deg); }
.sk-circle .sk-circle2:before {
  -webkit-animation-delay: -1.1s;
          animation-delay: -1.1s; }
.sk-circle .sk-circle3:before {
  -webkit-animation-delay: -1s;
          animation-delay: -1s; }
.sk-circle .sk-circle4:before {
  -webkit-animation-delay: -0.9s;
          animation-delay: -0.9s; }
.sk-circle .sk-circle5:before {
  -webkit-animation-delay: -0.8s;
          animation-delay: -0.8s; }
.sk-circle .sk-circle6:before {
  -webkit-animation-delay: -0.7s;
          animation-delay: -0.7s; }
.sk-circle .sk-circle7:before {
  -webkit-animation-delay: -0.6s;
          animation-delay: -0.6s; }
.sk-circle .sk-circle8:before {
  -webkit-animation-delay: -0.5s;
          animation-delay: -0.5s; }
.sk-circle .sk-circle9:before {
  -webkit-animation-delay: -0.4s;
          animation-delay: -0.4s; }
.sk-circle .sk-circle10:before {
  -webkit-animation-delay: -0.3s;
          animation-delay: -0.3s; }
.sk-circle .sk-circle11:before {
  -webkit-animation-delay: -0.2s;
          animation-delay: -0.2s; }
.sk-circle .sk-circle12:before {
  -webkit-animation-delay: -0.1s;
          animation-delay: -0.1s; }

@-webkit-keyframes sk-circleBounceDelay {
  0%, 80%, 100% {
    -webkit-transform: scale(0);
            transform: scale(0);
  } 40% {
    -webkit-transform: scale(1);
            transform: scale(1);
  }
}

@keyframes sk-circleBounceDelay {
  0%, 80%, 100% {
    -webkit-transform: scale(0);
            transform: scale(0);
  } 40% {
    -webkit-transform: scale(1);
            transform: scale(1);
  }
}


h1 {font: bold 34px "Century Schoolbook", Georgia, Times, serif;
    color: #333;
    font-size: 48px;
    line-height: 90%;
    margin: .2em 0 .4em 0;
    letter-spacing: -2px;
}

.itemname {
vertical-align: middle;
text-align: center;
}

% for item in items:

#{{item.id()}} {
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center; 

    background-image: url('/static{{item.openLink()}}');
}
% end


</style>
</head>
<body>

<div id="fullpage">
    <a id="backlink"  href="{{navi.backLink()}}">{{navi.backLink()}}</a>


    % if navi.hasPrevLink():
    <div class="section" data-prevlink="1">

<a id="prevlink" class="xyz" href="{{navi.prevLink()}}"><h1></h1></a>
<!--
<div class="sk-circle">
  <div class="sk-circle1 sk-child"></div>
  <div class="sk-circle2 sk-child"></div>
  <div class="sk-circle3 sk-child"></div>
  <div class="sk-circle4 sk-child"></div>
  <div class="sk-circle5 sk-child"></div>
  <div class="sk-circle6 sk-child"></div>
  <div class="sk-circle7 sk-child"></div>
  <div class="sk-circle8 sk-child"></div>
  <div class="sk-circle9 sk-child"></div>
  <div class="sk-circle10 sk-child"></div>
  <div class="sk-circle11 sk-child"></div>
  <div class="sk-circle12 sk-child"></div>
</div>
-->
    </div>
    % end

    % for item in items:
    % ooo = 'active' if item.isActive else ''


    <div class="section {{ooo}}">

        <div class="slide">
            <div class="itemname">

<!--
<div class="sk-circle">
  <div class="sk-circle1 sk-child"></div>
  <div class="sk-circle2 sk-child"></div>
  <div class="sk-circle3 sk-child"></div>
  <div class="sk-circle4 sk-child"></div>
  <div class="sk-circle5 sk-child"></div>
  <div class="sk-circle6 sk-child"></div>
  <div class="sk-circle7 sk-child"></div>
  <div class="sk-circle8 sk-child"></div>
  <div class="sk-circle9 sk-child"></div>
  <div class="sk-circle10 sk-child"></div>
  <div class="sk-circle11 sk-child"></div>
  <div class="sk-circle12 sk-child"></div>
</div>
-->

            </div>
        </div>

% if item.isDir():
            <div class="slide active">
% end
% if not item.isDir():
            <div id="{{item.id()}}" class="slide active">
% end

% if item.isDir():
            <div class="itemname">
            <h1>{{item.name()}}</h1>
            </div>
% end
        </div>

        % if item.isDir():
        <div class="slide"> 
            <div style="width:50%; margin: 0 auto; text-align: center;">
<!--
<div class="sk-circle">
  <div class="sk-circle1 sk-child"></div>
  <div class="sk-circle2 sk-child"></div>
  <div class="sk-circle3 sk-child"></div>
  <div class="sk-circle4 sk-child"></div>
  <div class="sk-circle5 sk-child"></div>
  <div class="sk-circle6 sk-child"></div>
  <div class="sk-circle7 sk-child"></div>
  <div class="sk-circle8 sk-child"></div>
  <div class="sk-circle9 sk-child"></div>
  <div class="sk-circle10 sk-child"></div>
  <div class="sk-circle11 sk-child"></div>
  <div class="sk-circle12 sk-child"></div>
</div>
-->
            <a class="xyz" href="{{item.openLink()}}"><h1> </h1></a>
            </div>
        </div>
        % end

    </div>
    % end

% if navi.hasMoreLink():
    <div class="section" data-morelink="1">
            <div style="width:50%; margin: 0 auto; text-align: center;">
<!--
<div class="sk-circle">
  <div class="sk-circle1 sk-child"></div>
  <div class="sk-circle2 sk-child"></div>
  <div class="sk-circle3 sk-child"></div>
  <div class="sk-circle4 sk-child"></div>
  <div class="sk-circle5 sk-child"></div>
  <div class="sk-circle6 sk-child"></div>
  <div class="sk-circle7 sk-child"></div>
  <div class="sk-circle8 sk-child"></div>
  <div class="sk-circle9 sk-child"></div>
  <div class="sk-circle10 sk-child"></div>
  <div class="sk-circle11 sk-child"></div>
  <div class="sk-circle12 sk-child"></div>
</div>
-->
<a id="morelink" class="xyz" href="{{navi.moreLink()}}"><h1></h1></a>
            </div>
    </div>
% end

</div>

<a id="nextLink" href="/f/i/idx_next/l/3/p/cur_path">{{next}}</a>

<script>

$(document).ready(function() {
    $('#fullpage').fullpage(
{
loopHorizontal: false,
verticalCentered: true,
afterLoad: function(anchorLink, slideIndex)
{
console.log(slideIndex)
    if ($(this).attr('data-morelink') == "1")
    {
        document.location = $("#morelink").attr('href');
    }
    if ($(this).attr('data-prevlink') == "1")
    {
        document.location = $("#prevlink").attr('href');
    }
},
sectionsColor: ['#ffc40d', '#2b5797', '#eff4ff', '#00aba9', '#1d1d1d'],
touchSensitivity: 1,
normalScrollElementTouchThreshold: 1,

afterSlideLoad: function(anchorLink, index, slideAnchor, slideIndex) {
console.log(anchorLink+" "+slideIndex);
//console.log($(this).find(".xyz")[0].attr('href'));
if (slideIndex == 0)
{
    document.location = $("#backlink").attr('href');
}
if (slideIndex == 2)
{
console.log("00000:");
    console.log($(this)[0]);
    console.log($(this).find(".xyz").attr('href'));
    document.location = $(this).find(".xyz").attr('href');
}

}    
}

);
});


$(document).ready(function() {
 
console.log("ready");
    //tutaj nasze skrypty jquery
 
// if a key is pressed and then released
$(document).keydown(function(e) {

console.log("keydown"+e.which);
});
$(document).keypress(function(e) {

console.log("bind"+e.which);
  // ...and it was the enter key...
  if(e.which == 13) {

    // ...navigate to the associated URL.
    document.location = $("#nextLink").attr('href');
  }               
});
})
</script>
</body>
</html>
"""

#

@route('/')
def red():
    redirect('/s/non/d/none/i/0/c/5/r/')

class Navi(object):
    def __init__(self):
        self.link = None
        self.index = 0
        self.count = 10
        self.files_count = 0

    def backLink(self):
        return os.sep + 's' + os.sep + self.link.rsplit('/', 2)[1] + '/d/none' + '/i/0/c/4' + self.link.rsplit('/', 2)[0] + os.sep

    def hasPrevLink(self):
        if self.index == 0:
            return False
        return True
    def hasMoreLink(self):
        print "jasMore", self.index, self.files_count
        if self.index + self.count >= self.files_count:
            return False
        return True
    
    def prevLink(self):
        return os.sep + 's' + os.sep + self.link.rsplit('/', 2)[1] + '/d/up' + '/i/'+str(self.index-self.count)+'/c/'+str(self.count) + self.link 

    def moreLink(self):
        return os.sep + 's' + os.sep + self.link.rsplit('/', 2)[1] + '/d/down' + '/i/'+str(self.index+self.count)+'/c/'+str(self.count) + self.link 

    def __str__(self):
        return "%s, %s %s" % (self.link, self.backLink(), 'x')

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()


class Item(object):
    def __init__(self):
        self.path = None
        self.isActive = False
        self.isDirx = None
        self.dirNamex = None
        self.navi = None

    def isDir(self):
        if self.isDirx == None:
            self.isDirx = os.path.isdir(self.path)
        return self.isDirx

    def name(self):
        return self.dirName()

    def dirName(self):
        if self.dirNamex == None:
            self.dirNamex = self.path.rsplit('/')[-1]
        return self.dirNamex
    
    def id(self):
        return self.path.replace('/', '_').replace('.','_').replace(' ', '_').replace('(', '_').replace(')', '_')

    def openLink(self):
        if self.isDir():
            return '/s/%s/d/none/i/%i/c/%i/r/%s/' % (self.dirName(),0, self.navi.count, self.path.split(os.sep, 1)[1])
        
        l = os.sep + self.path.split(os.sep, 1)[1] 
        return l.replace(' ', '%20')

    def __lt__(self, other):
        if other.isDir() and not self.isDir():
            return False
        if not other.isDir() and self.isDir():
            return True

        return other.dirName() > self.dirName()

    def __str__(self):
        return "\n++%s, %s %s, %s, %s++\n" % (self.path, self.isDir(), self.openLink(), self.dirName(), str(self.isActive))

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()


@route('/s/<select>/d/<direction>/i/<index:int>/c/<count:int>/r/')
def root(select, direction, index, count):
    path = os.curdir + os.sep
    return callbackxx(select, 'none', index, count, path)
#    navi = Navi()
#    navi.link = '/r/'
#    items = os.listdir('.')
#    iii = []
#    for i in items:
#        it = Item()
#        it.path = path + os.sep + i
#        it.isDir = os.path.isdir(it.path)
#        print it
#        iii.append(it)
#    return template("AAAAAA, {{items}}, |{{it}}|", items=iii, it=items[0] )
ona = """
{{path}}
<br/>
% for i in items:
{{i}}
<br/>
% end
<br/>
{{navi}}
"""
@route('/s/<select>/i/<index:int>/c/<count:int>/r/<path:path>')
def bbbb(select, index, count, path):
    return callbackxx(select, 'none', index, count, path)

@route('/s/<select>/d/<direction>/i/<index:int>/c/<count:int>/r/<path:path>')
def callbackxx(select, direction, index, count, path):
    print select, direction, index, count, path
    navi = Navi()
    navi.index = index
    navi.count = count 
#    navi.direction = direction
    navi.link = '/r/' + path
    if path is '':
        path = '.'
    print '1'
    #items = os.listdir('./'+path)
    x = next(os.walk('./'+path))
    itemsd = x[1]
    itemsf = x[2]
    print '2a'
    itemsd = sorted(itemsd)
    itemsf = sorted(itemsf)
    navi.files_count = len(itemsf)
    print '2b'
    iii = []
    dirsc = 0
    print '3'
    if index == 0:
        for i in itemsd:
            print '3.'
            it = Item()
            it.navi = navi
            it.path = os.curdir + os.sep + path + i
            it.isDirx = True
            #if it.isDir() and index == 0:
            #    dirsc=dirsc+1
            if it.dirName() == select:
                it.isActive = True

            #if (int(index) == 0 and it.isDir()) or not it.isDir():
            iii.append(it)

    for i in itemsf[index:index+count]:
        it = Item()
        it.path = os.curdir + os.sep + path + i
            
        #if it.isDir() and index == 0:
        #    dirsc=dirsc+1
        #if it.dirName() == select:
        #    it.isActive = True

        #if (int(index) == 0 and it.isDir()) or not it.isDir():
        iii.append(it)

    if len(itemsf[index:index+count]) > 0:
        if direction == 'up':
            iii[-1].isActive = True
        elif direction == 'down':
            iii[0].isActive = True

    print '4a'
        #iii = sorted(iii)
    print '4b'
    for x in iii:
        print x

    print index, index+dirsc+count
    return template(templ, navi=navi,  path=path, items=iii)


@route('/r/<path:path>')
def callback(path):
    navi = Navi()
    navi.link = '/r/' + path
    print path
    if path is '':
        path = '.'
    else:
        path = os.curdir + os.sep + path
    print path
    items = os.listdir(path)
    iii = []
    for i in items:
        it = Item()
        it.path = path + i
        #it.isDir = os.path.isdir(it.path)
        print it
        iii.append(it)
    return template("AAAAAA{{path}}, {{items}} {{navi}}", navi=navi,  path=path, items=iii)




@route('/hello/<name>')
def indexx(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='.')

run(host='192.168.1.105', port=8080)

