import requests
import pystache
import json

from IPython.core.display import HTML

ENV = {}

def setENV(envObj):
    global ENV 
    ENV = envObj
    
def showenv():
    return ENV

def GET(url, *args,**kargs):
    url = pystache.render(url, ENV)
    r = requests.get(url, **kargs )
    return r



def POST(url, body=None, *args,**kargs):
    with open (body, "r") as myfile:
        data=myfile.read()
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