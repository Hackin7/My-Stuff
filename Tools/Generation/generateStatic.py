from jinja2 import Template

with open('templates/overall.html', 'r') as f: 
    templateOverall = Template(f.read())


"""
    <div id="welcome-section" style="height:50vh;">
      <div class="intro">
        <h1>{{title}}</h1>
      </div>
    </div>
    <br><br>
    <div class="content">
    {{content|safe}}
      
    </div>
"""


MAINDIR = "../../"

staticPages = ["about.html", "index.html", "achievements.html", "links.html"]
for pageName in staticPages:
    with open("content/"+pageName, "r") as f:
        with open(MAINDIR + pageName, 'w') as out:
            out.write(templateOverall.render(title=pageName[:-4], content = f.read()))

