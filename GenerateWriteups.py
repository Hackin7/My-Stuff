import os
import shutil

from jinja2 import Template

with open('Tools/Generation/templates/overall.html', 'r') as f: 
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

def generateDirectory(hierarchy):
    newpath = "./Generated/"+'/'.join(hierarchy[2:])
    os.makedirs(newpath, exist_ok=True)
    return newpath
    
for root, dir, files in os.walk("../Solutions/Cyber Security/Capture the Flag Competitions"):
    root = root.replace('\\', '/')
    hierarchy = root.split("/")
    if len(hierarchy) > 8: continue
    
    for filename in fnmatch.filter(files, "*"):
        path = str(root + "/" + filename)
        
        if filename == "README.md":
            print(path)
            try:
                with open(path, 'r') as f:
                    html = textToMarkdown(f.read())
                    
                newpath = generateDirectory(hierarchy)
                
                with open(newpath+ "/main.html", 'w', encoding='utf-8') as f:
                    f.write(markdownTemplate(html, path[len("../Solutions/"):]))
                    
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
        
with open("./links.html", "w", encoding='utf-8') as f:
    links = "<ol>"
    for i in generated:
        links += f"<li><a href='{i}'>{i}</a></li>"
    links += "</ol>"
    f.write('<link href="/github-markdown-css/github-css.css" rel="stylesheet"/>'+"<h1>CTF Writeups</h1>"+links)
