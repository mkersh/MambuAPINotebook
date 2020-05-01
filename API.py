import requests
import pystache
import json
import uuid
import ast

from IPython.core.display import HTML

ENV = {}

def setENV(envObj):
    global ENV 
    ENV = envObj
    
def showenv():
    return ENV

def GETOld(url, *args,**kargs):
    url = pystache.render(url, ENV)
    r = requests.get(url, **kargs )
    return r

def GET(url, headerparts=None, *args,**kargs):
    if headerparts is not None:
        headers = pystache.render(str(kargs['headers']), headerparts)
        headers = ast.literal_eval(headers)
        kargs['headers'] = headers
    url = pystache.render(url, ENV)
    r = requests.get(url, **kargs )
    return r



def POST(url, body=None, bodyparts=None, headerparts=None, *args,**kargs):
    if headerparts is not None:
        headers = pystache.render(str(kargs['headers']), headerparts)
        headers = ast.literal_eval(headers)
        kargs['headers'] = headers
    if body is None:
        url = pystache.render(url, ENV)
        r = requests.post(url, data="{}", **kargs )
        return r
    else:
        with open (body, "r") as myfile:
            data=myfile.read()
            if bodyparts is not None:
                data = pystache.render(data, bodyparts)
            url = pystache.render(url, ENV)
            r = requests.post(url, data=data, **kargs )
            return r
        
# remove below once certain above new version doesn't break anything
def POSTOld(url, body=None, bodyparts=None, *args,**kargs):
    if body is None:
        url = pystache.render(url, ENV)
        r = requests.post(url, data="{}", **kargs )
        return r
    else:
        with open (body, "r") as myfile:
            data=myfile.read()
            if bodyparts is not None:
                data = pystache.render(data, bodyparts)
            url = pystache.render(url, ENV)
            r = requests.post(url, data=data, **kargs )
            return r

def POST2(url, data=None, bodyparts=None, *args,**kargs):
    if data is None:
        url = pystache.render(url, ENV)
        r = requests.post(url, data="{}", **kargs )
        return r
    else:
        if bodyparts is not None:
            data = pystache.render(data, bodyparts)
        url = pystache.render(url, ENV)
        r = requests.post(url, data=data, **kargs )
        return r
    

        
def PATCH(url, body=None, *args,**kargs):
    with open (body, "r") as myfile:
        data=myfile.read()
        url = pystache.render(url, ENV)
        r = requests.patch(url, data=data, **kargs )
        return r
    
def PUT(url, body=None, *args,**kargs):
    with open (body, "r") as myfile:
        data=myfile.read()
        url = pystache.render(url, ENV)
        r = requests.put(url, data=data, **kargs )
        return r
    
def DELETE(url, *args,**kargs):
    url = pystache.render(url, ENV)
    r = requests.delete(url, **kargs )
    return r

def PRINT(r):
    print ("API status: ", end="")
    print(r.status_code)
    print ("JSON Response:")
    try:
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    except:
        print("NO Content")
    
def PRINTHTML(htmlStr):
    HTML(htmlStr)
    
    
# -------------------------------------------------------------------------------
# Other helper functions

def getUUID():
    return str(uuid.uuid4())

def writeFile(jsonDictOrStr, fileName):
    if isinstance(jsonDictOrStr, dict):
        jsonStr = json.dumps(jsonDictOrStr)
    else:
        jsonStr = jsonDictOrStr
    with open (fileName, "w") as myfile:
        myfile.write(jsonStr)
        
def readFile(fileName):
    with open (fileName, "r") as myfile:
        return myfile.read()
    
def expandPlaceholders(fileName, placeholders):
    fileStr = readFile(fileName)
    fileStr = pystache.render(fileStr, placeholders)
    writeFile(fileStr, fileName)
    fileStr = readFile(fileName)
    return fileStr
    
# -------------------------------------------------------------------------------
# Other more specific printing/output options

cc = 0
def printCount():
    global cc
    cc = cc + 1
    return "[{0}]".format(cc)

def printCustomers(r):
    global cc
    cc = 0
    obj = {
            'customers': r.json(),
            'outer': printCount
    }
    print(pystache.render("{{#customers}} {{outer}} {{firstName}} {{lastName}}\n {{/customers}}", obj))