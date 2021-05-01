import sys
sys.path.append('../')
from tools import *

import os

### Reading Data ###############################################################
def conversion_func(row):
    '''
    Customise this function to fit whatever specification needed
    '''
    ## Terminating Case
    if str(row["Name"]) == "nan": #Nothing left
        return None

    ## Formatting Stuff
    entry = {}
    entry["name"] = Excel.read(row["Name"])
    entry["date"] = Excel.read(row["Date"])
    entry["filepath"] = Excel.read(row["File Path"])

    ## Tagging
    entry["tags"] = {}
    for c in ["Category"]:
        entry["tags"][c] = Excel.readList(row[c], ', ')

    return entry

### Conversion of Data #########################################################
def htmlConversion(rootdir, posts):
    if rootdir[-1] != '/':
        rootdir += '/'

    for i in range(len(posts)):
        oldpath = rootdir+posts[i]['filepath']
        with open(oldpath, 'r') as f:
            data = textToMarkdown(f"{posts[i]['date']}\n"+f.read())
        os.system(f'rm {formatDir(oldpath)}')

        newpath = rootdir+posts[i]['filepath']+'.html'
        with open(newpath, 'w') as f:
            f.write(data)
        posts[i]['htmlpath'] = posts[i]['filepath']+'.html'
    return posts

### Main #######################################################################
def formatDir(dir):
    return dir.replace(" ", '\ ')

def generate(dir='./', contentdir='Content', newdir='/tmp/stuff'):
    if contentdir[-1] != '/':contentdir += '/'
    if newdir[-1] != '/':newdir += '/'

    #os.system(f"rm -rf {newdir}/*")
    generateDirectory(newdir)
    os.system(f"cp -r {formatDir(contentdir)}* {formatDir(newdir)}")

    posts = Excel.readSheet(dir+'Blogging.xlsx', 'Posts', conversion_func)
    posts = htmlConversion(newdir, posts)
    return posts

#generate()
