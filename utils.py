from datetime import datetime
import os.path
from os import path

import pytz
import ast


#--- DATE -----
def getDateStr():
    now = datetime.now()
    #print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y%m%d")
    #print("date=", dt_string)
    return dt_string

def getTimeStr():
    now = datetime.now()
    #print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H%M%S")
    #print("time =", dt_string)
    return dt_string

def getDateTime(dt_format='%Y%m%d%H%M%S'):
    now = datetime.now()
    #print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime(dt_format)
    #print("date and time =", dt_string)
    return dt_string

def createFolder(folder):
    if(path.exists(folder)==False):
        try:
            os.mkdir(folder)
        except OSError:
            print ("Creation of the directory %s failed" % folder)
        else:
            print ("Successfully created the directory %s " % folder)



def getCurrentTime():
    return datetime.now(tz=pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%dT%H:%M:%SZ')

#Convert json to dict
def json2Dict(data_json): 
    data_str = "{0}".format(data_json)
    data_dict = ast.literal_eval(data_str)
    #print(type(data))
    return data_dict 

#getDateStr();
#getTimeStr();
#getDateTime();