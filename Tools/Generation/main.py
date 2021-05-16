import sys
sys.path.append('../')
from tools import *
import os

#import GenerateWriteups

from jinja2 import Template
with open('templates/overall.html', 'r') as f:
    templateOverall = Template(f.read())

### Blogging Code ##############################################################
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
os.system(f"cp -r {blogGenerate.formatDir(olddir)}* {blogGenerate.formatDir(newdir)}")

for i in range(len(posts)):
    with open(olddir+posts[i]['htmlpath'], 'r') as f:
        data = f.read()


    paths = os.path.split(posts[i]['htmlpath'])
    if len(paths) > 1:
        generateDirectory(os.path.join(newdir, *paths[:-1]))

    posts[i]['fullpath'] = newdir+posts[i]['htmlpath']
    with open(posts[i]['fullpath'], 'w') as f:
        data = f"<div class='content'><br>{data}</div>"
        data = templateOverall.render(name=posts[i]['name'], content=data)
        f.write(data)

writeAsJson(posts, '../../js/blogposts.js')

### CTF Writeup Code ###########################################################
sys.path.append('./Writeups Generator')
import writeup_scraper
writeup_scraper.NEW_PATH_ROOT =  "../../Generated/CTF_Writeups"
os.system(f"rm -rf {writeup_scraper.NEW_PATH_ROOT}")
writeup_scraper.findCTF("CTF Writeups","/run/media/hacker/Windows/Users/zunmu/Documents/Stuff/Github/Solutions/Cyber Security/Capture the Flag Competitions")

with open("content/links.html", "w", encoding='utf-8') as f:
    ctf_links = "<ol>"
    for i in writeup_scraper.ctf_writeups:
        year, ctf_name, relative_path = i
        new_path = os.path.join("/Generated/CTF_Writeups", relative_path, "index.html")
        ctf_links += f"<li><a href='{new_path}'>({year}) {ctf_name}</a></li>\n"
    ctf_links += "</ol>"

    links = "<ol>"
    for i in writeup_scraper.chall_writeups:
        year, ctf, category, chal, relative_path = i
        new_path = os.path.join("/Generated/CTF_Writeups", relative_path, "index.html")
        if category != "":
            category = f"[{category}]"
        links += f"<li><a href='{new_path}'>({year}) {ctf}: {category} {chal}</a></li>\n"
    links += "</ol>"

    f.write("""
    <div id="welcome-section" style="height:20vh;">
          <div class="intro">
            <h1>CTF Writeups</h1>
          </div>
        </div>
    </div>
    <br>
    """+#'<link href="/github-markdown-css/github-css.css" rel="stylesheet"/>' +
    f"""
    <div class='content'>
        <h2>CTF Writeups</h2>
        {ctf_links}
        <h2>Writeup links</h2>
        {links}
    </div>
    """)


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
