import os
import shutil
import fnmatch
import writeupTemplateGenerate
import sys; sys.path.append('../')
from tools import *

def get_files(root):
    folders = []
    files = []
    for item in os.listdir(root):
        if os.path.isfile(os.path.join(root, item)):
            files.append(item)
        else:
            folders.append(item)
    return folders, files

def match(files, writeup_files=["README.md", "solve.py"]):
    for f in writeup_files:
        if f in files:
            return True
    return False

def genGithubLink(path, isFolder=False, from_root = "Cyber Security/Capture the Flag Competitions/"):
    if not isFolder:
        github = "https://github.com/Hackin7/Programming-Crappy-Solutions/blob/master/"
    else:
        github = "https://github.com/Hackin7/Programming-Crappy-Solutions/tree/master/"
    return github + from_root + path

def copy_dir(data, root, files, newroot, list):
    #list.append(files)
    generateDirectory(newroot)
    if match(files):
        list.append(data)
        for file in files:
            old_path = os.path.join(root, file)
            new_path = os.path.join(newroot, file)
            if file == "README.md":
                new_path += ".html"
                with open(old_path, "r") as f:
                    given_data = textToMarkdown(f.read())

                new_path = os.path.join(newroot, "index.html")
                with open(new_path, "w") as f:
                    link = genGithubLink(data[-1])
                    final_data = writeupTemplateGenerate.generateTemplate(link, given_data)
                    f.write(final_data)

            if file[-4:] in (".png", ".jpg", ".bmp"):
                #print(old_path, new_path)
                shutil.copyfile(old_path,  new_path)

def categoryMapping(cat):
    mappings = {
        "Web":["Web Services"],
        "Cloud":[],
        "Reverse Engineering":["RE", "Reversing", "Rev", "Mobile"],
        "Binary Exploitation":["Pwn", "Binary"],
        "Miscellaneous":["Misc"],
        "Forensics":["Network Services"],
        "Data Science":[],
        "Crypto":[],
        #"":[],
    }
    if mappings.get(cat) != None:
        return cat
    else:
        for proper_cat, all_cats in mappings.items():
            for c in all_cats:
                if c == cat:
                    return proper_cat
        return ""


###########################################################

ctf_writeups = []
chall_writeups = []
NEW_PATH_ROOT = "/tmp"
#NEW_PATH_ROOT = "../../../Generated/CTF_Writeups"
#NEW_PATH_ROOT =  "../../Generated/CTF_Writeups" #"/tmp"

def getRelativePath(prev_folders):
    return os.path.join(prev_folders[0], *prev_folders[1:])

def findCTF(folder, path, prev_folders=[]):
    folders, files = get_files(path)
    if "README.md" in files:
        year = prev_folders[0]
        ctf_name = " ".join(prev_folders[1:])
        relative_path = getRelativePath(prev_folders)
        new_path = os.path.join(NEW_PATH_ROOT, relative_path)

        findChal(year, ctf_name, path, prev_folders)
        copy_dir( (year, ctf_name, relative_path) , path, files, new_path, ctf_writeups )
    else:
        for folder in folders:
            new_path = os.path.join(path, folder)
            findCTF(folder, new_path, prev_folders+[folder])


def findChal(year, ctf, path, prev_folders):
    folders, files = get_files(path)
    for category in folders:
        cat_path = os.path.join(path, category)
        cat_folders, cat_files = get_files(cat_path)

        relative_path = getRelativePath(prev_folders + [category])

        copy_dir( (year, ctf, categoryMapping(category), category, relative_path) , cat_path, cat_files, os.path.join(NEW_PATH_ROOT, relative_path), chall_writeups )

        for chal in cat_folders:
            relative_path = getRelativePath(prev_folders + [category, chal])

            chal_path = os.path.join(cat_path, chal)
            chal_folders, chal_files = get_files(chal_path)
            copy_dir( (year, ctf, categoryMapping(category), chal, relative_path) ,
                     chal_path, chal_files,
                     os.path.join(NEW_PATH_ROOT, relative_path),
                     chall_writeups )

if __name__ == "__main__":
    findCTF("CTF Writeups","/run/media/hacker/Windows/Users/zunmu/Documents/Stuff/Github/Solutions/Cyber Security/Capture the Flag Competitions")
    print(ctf_writeups)
    print(chall_writeups)
################################################################################
def writeToExcel():
    import pandas as pd
    df1 = pd.DataFrame(ctf_writeups)
    df2 = pd.DataFrame(chall_writeups)
    with pd.ExcelWriter('/tmp/output.xlsx') as writer:
        df1.to_excel(writer, sheet_name='CTFs')
        df2.to_excel(writer, sheet_name='Challenges')
