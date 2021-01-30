from API import *
from ENV import *
import time
import os
import hashlib

 # Make a signature to sign the request
# Signature: hex( sha1({GMT_UNIXTIME} + {API_SECRET} + {CONTENT} + {API_SECRET}) )
def make_sign(secret, timestamp, content):
    s = (str(timestamp) + secret + content + secret).encode('utf-8')
    return hashlib.sha1(s).hexdigest()

def getTraceItem(i):
    data = """
    {
        "timeout": 30,
        "ops": [{
            "company_id": "i962764498",
            "conv_id": 27845,
            "type": "create",
            "obj": "task",
            "data": {
                "index": {{i}} 
            }
        }]
    }
    """
    
    HEADERS = {"Content-Type": "application/json"} 
    PARAMS = {}
    bodyparts = {"i": i}
    data = pystache.render(data, bodyparts)
    unixtime = int(time.time()) 
    secret = ENV["mpo1"] 
    signature = make_sign(secret, unixtime, data)
    mpoSyncUrl = "https://mpo-multitenant-syncapi.mambuonline.com/api/1/json/214/" + str(unixtime) +  "/" + signature
    # s = time.perf_counter()
    r = POST2(mpoSyncUrl, headers=HEADERS, params=PARAMS, data=data)
    # elapsed = time.perf_counter() - s
    # print(f"Time Taken (secs) to Execute: {elapsed}")
    # print("data = ", data)
    # print("signature", signature)
    # PRINT(r)
    return r.json()["ops"][0]["data"]["TRACE"]

def main():
    i = 0
    traceItems = getTraceItem(-1)
    i = len(traceItems)
    for traceItem in traceItems:
            print(traceItem)

    while True:
        traceItem = getTraceItem(i)[0]   
        while (traceItem!=None):
            print(traceItem)
            i += 1
            traceItem = getTraceItem(i)[0]
        g = input("0 - Reset, c - Clear, Other Key - Read Next ") 
        if (g == "0"):
            i = 0
            return main()
        elif (g == "c"):
            getTraceItem(-2)
            # Not sure why?? but I need to call twice
            getTraceItem(-2)
            i = 0
        
    
    
if __name__ == '__main__':
	main()