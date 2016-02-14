from bottle import route, run, template, static_file
import os

templ = """
<html>
<head>
 
<script src="http://code.jquery.com/jquery-latest.min.js"></script> 
<!-- <script src="https://npmcdn.com/masonry-layout@4.0/dist/masonry.pkgd.js"></script> -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/freewall/1.0.5/freewall.min.js"></script>
<style>


/* fluid 5 columns */
//.grid-sizer,
.grid-item { width: 100px; height:100px;}
/* 2 columns wide */
//.grid-item--width2 { width: 40%; }
//.grid {height: 90%; width:90%; }
//.iii {max-width:200px;}
</style>
</head>
<body>
<a href="/f/i/0/l/3/p/{{back}}">{{back}}</a>


<ul>
% for item in dirs:
<li>
<a href="/f/i/0/l/3/p/{{item}}">{{item}}</a>
</li>
% end
</ul>

<div class="grid">
% for item in files:
<img class="grid-item"  src="/static{{item}}" alt="Smiley face">
% end
</div>

<a id="nextLink" href="/f/i/{{idx_next}}/l/3/p/{{cur_path}}">{{next}}</a>

<script>

$(document).ready(function() {
//$('selector').masonry();
 
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

});

$(window).load(function(){


//      var wall = new Freewall(".grid");
 //   wall.reset({
 // selector: '.brick',
 // animate: true,
 // cellW: 100,
 // cellH: 100
//});
//        wall.fitZone($(window).width() - 30 , screen.height - 30);
//        wall.fitZone(800 , 800);

                var wall = new Freewall(".grid");
/*
                wall.reset({
                    selector: '.grid-item',
                    animate: false,
                    cellW: 160,
                    cellH: 160,
                    delay: 30,
                    onResize: function() {
                        wall.refresh($(window).width() - 30, $(window).height() - 30);
                    }
                });
*/
                // caculator width and height for IE7;
                //wall.fitZone($(window).width() - 30 , $(window).height() - 30);
                //wall.fitZone(500,500);
                wall.fitWidth();



//    $('.grid').masonry({
    // options
 //   itemSelector: '.grid-item',
//percentPosition: true,
//columnWidth: 200,
// do not use .grid-sizer in layout
//itemSelector: '.grid-item'

  // });
});

</script>
</body>
</html>
"""

@route('/b/<path:path>')
def callback(path):
    items = os.listdir('./'+path)
    return template("AAAAAA{{path}}, {{items}}", path=path, items=items)

@route('/f/i/<idx:int>/l/<le:int>/p/<path:path>')
def index(idx, le, path):
    back = path.rsplit('/', 1)[0]
    idx_next = idx+3
    print path
    items = os.listdir('./'+path)
    print "AA", items
    files = []
    dirs = []
    for i in items:
        print i
        if os.path.isdir('./'+path+'/'+i):
            dirs.append(path+'/'+i)
        else:
            files.append(path+'/'+i)
    print '000:', dirs
    print '999:', files
            
    #return template('<b>Hello {{name}}</b>!', name=dirs)
    return template(templ, cur_path=path, dirs=dirs, files=files[idx:idx+le], back=back, idx_next=idx_next)

@route('/hello/<name>')
def indexx(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='.')

run(serverl="tornado", host='192.168.1.102', port=8080)

