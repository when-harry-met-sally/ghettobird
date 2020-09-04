from pprint import pprint
from datetime import datetime
import json
from helpers import getTree

log = []
def errorLog(source, message):
    now = datetime.now() 
    time = now.strftime("%H:%M:%S, %m/%d/%Y")
    log.append([time, source, message])
    print(time + " | " + source + " | " + message)
    
def run(routine):
    return routine["method"]["type"](routine)