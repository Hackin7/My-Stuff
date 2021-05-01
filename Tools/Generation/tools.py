import pycmarkgfm
def textToMarkdown(text):
    return pycmarkgfm.gfm_to_html(text)


import os
def generateDirectory(path):
    os.makedirs(path, exist_ok=True)

### Excel Functions ########################################################################

import pandas as pd
import json

class Excel:
    ### Excel Processing ##############################################################
    def readSheet(xlsx, sheet_name, conversion_func):
        df = pd.read_excel(xlsx,  sheet_name)

        output = []
        counter = 0
        for rowIndex in range(df.shape[0]): # Number of rows
            row = df.iloc[rowIndex]

            ### Add custom processing code
            value = conversion_func(row)
            if value == None:
                break
            else:
                output.append(value)

            counter += 1
        print(counter)
        return output

    ### Converting Each Record to appropriate format ####################################

    def read(field):
        string = str(field)
        if string == "nan" or string == '-':
            return ""
        else:
            return str(field)

    def readList(string, delimiter='|'):
        string = str(string)
        if string == 'nan' or string == '-':
            return []
        else:
            return string.split(delimiter)

### Writing as a file to be imported by HTML code #################################
def writeAsJson(data, filename):
    jsonData = json.dumps(data)
    with open(filename, 'w') as outfile:
        outfile.write("var taggingSystemData = "+jsonData+";")
