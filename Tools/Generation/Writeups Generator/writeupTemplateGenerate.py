from jinja2 import Template
try:
    with open('../templates/overall.html', 'r') as f:
        templateOverall = Template(f.read())
except:
    with open('./templates/overall.html', 'r') as f:
        templateOverall = Template(f.read())

def generateTemplate(link, given_data):

    data = f"""
    <div class='content'>
    <link href='/css/github-css.css' rel='stylesheet' type='text/css'>
        <br>
        <a href='{link}'>Original Github Link</a><br>
        {given_data}
    </div>
    """
    return templateOverall.render(title="CTF Writeup", content=data)
