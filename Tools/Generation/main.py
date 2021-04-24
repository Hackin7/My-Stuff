import sys
sys.path.append('../')
from tools import *


#import GenerateWriteups

from jinja2 import Template
with open('templates/overall.html', 'r') as f:
    templateOverall = Template(f.read())

### Blogging Code ##############################################################
import sys
sys.path.append('./Blogging System')
import blogGenerate

olddir = '/tmp/stuff/'
newdir = '../../Generated/Blog/'

posts = blogGenerate.generate(
    dir='./Blogging System/',
    contentdir='./Blogging System/Content',
    newdir=olddir
)

generateDirectory(newdir)
for i in range(len(posts)):
    with open(olddir+posts[i]['htmlpath'], 'r') as f:
        data = f.read()

    posts[i]['fullpath'] = newdir+posts[i]['htmlpath']
    with open(posts[i]['fullpath'], 'w') as f:
        data = f"<div class='content'><br>{data}</div>"
        data = templateOverall.render(name=posts[i]['name'], content=data)
        f.write(data)

writeAsJson(posts, '../../js/blogposts.js')
################################################################################

MAINDIR = "../../"

staticPages = [
    "about.html",
    "index.html",
    "achievements.html",
    "links.html",
    "all_projects.html",
    "blog.html"
 ]
for pageName in staticPages:
    with open("content/"+pageName, "r") as f:
        with open(MAINDIR + pageName, 'w') as out:
            out.write(templateOverall.render(title=pageName[:-4], content = f.read()))
