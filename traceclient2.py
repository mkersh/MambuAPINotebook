from API import *
from ENV import *
import time
import os

def getTraceItem(i):
    data = """
    {
        "methodToCall": "https://mpo-multitenant.mambuonline.com/api/1/json/public/24326/288106d82551acf628173af5ec133678af28d495",
        "params": {
            "TraceSyncExample": 1,
            "index": {{i}}
        }	
    }
    """
    HEADERS = {}
    PARAMS = {}
    bodyparts = {"i": i}
    # s = time.perf_counter()
    r = POST2('http://ec2-35-177-46-123.eu-west-2.compute.amazonaws.com:8001', headers=HEADERS, params=PARAMS, data=data, bodyparts=bodyparts)
    # elapsed = time.perf_counter() - s
    # print(f"Time Taken (secs) to Execute: {elapsed}")
    # PRINT(r)
    return r.json()["TRACE"]

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