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

def PRINT(r):
    print ("API status: ", end="")
    print(r.status_code)
    print ("JSON Response:")
    print(json.dumps(r.json(), indent=4, sort_keys=True))
    
def PRINTHTML(htmlStr):
    HTML(htmlStr)