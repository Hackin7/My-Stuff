import os
import shutil

from jinja2 import Template

MAINDIR = "../../"
WRITEUPS_DIR = "../../../Solutions/Cyber Security/Capture the Flag Competitions"

with open('templates/overall.html', 'r') as f:
    writeupTemplate = Template(f.read())

import fnmatch
#import markdown2 as markdown
import pycmarkgfm
generated = []

def markdownTemplate(html, path=None):

    if path != None:
        link = "https://github.com/Hackin7/Programming-Crappy-Solutions/blob/master/"+ path
        html = f"<div><a href='{link}'>Original Github Link</a></div>" + html


    html = "<div class='github_markdown' style='width:80wh;'>" + html + "</div>"
    html = "<link href='/github-markdown-css/github-css.css' rel='stylesheet' type='text/css'>"+ html
    data = writeupTemplate.render( title="Writeup", content=html)
    return data

def textToMarkdown(text):
    #return markdown.markdown(text)
    return pycmarkgfm.gfm_to_html(text)

def generateDirectory(hierarchy, folder="/Solutions/Cyber Security/Capture the Flag Competitions"):
    newpath = MAINDIR + "Generated"+folder.replace(" ", "_")+'/'.join(hierarchy[6:])

    #print("GEN", newpath)#, hierarchy)
    os.makedirs(newpath, exist_ok=True)
    return newpath

for root, dir, files in os.walk(WRITEUPS_DIR):
    root = root.replace('\\', '/')
    hierarchy = root.split("/")
    if len(hierarchy) > 11: continue

    for filename in fnmatch.filter(files, "*"):
        path = str(root + "/" + filename)

        if filename == "README.md":
            print(path)
            try:
                with open(path, 'r') as f:
                    html = textToMarkdown(f.read())

                newpath = generateDirectory(hierarchy)

                with open(newpath+ "/main.html", 'w', encoding='utf-8') as f:
                    f.write(markdownTemplate(html, path[len(WRITEUPS_DIR):]))

                generated.append(newpath+"/main.html")
            except Exception as e:
                print("ERROR:",e)
                pass
        elif filename[-4:] in (".png", ".jpg", ".bmp"):
            try:
                newpath = generateDirectory(hierarchy)
                shutil.copyfile(path, newpath+"/"+filename)
            except Exception as e:
                print("ERROR:",e)

with open("content/links.html", "w", encoding='utf-8') as f:
    links = "<ol>"
    for i in generated:
        links += f"<li><a href='{i}'>{i}</a></li>\n"
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
    "<div class='content'>"+links+"</div>")
