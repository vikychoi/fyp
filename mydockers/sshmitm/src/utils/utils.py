import os
import io
import json

def logToJson(hostname,username,password,accessTime,IP,event,file_path=""):
    store_path='log/sshmitm.json'
    #store_path='/home/lmk/fyp/mydockers/sshmitm/src/log/sshmitm.json'

    log={}
    log['username']=username
    log['password']=password
    log['access_time']=accessTime
    log['ip']=IP
    log['event']=event
    

    if event=='logged_in':
        log['sshCommand']=[]
        log['log.file.path']=file_path
        with open(file_path, 'r',encoding='UTF-8') as open_file:
            content = open_file.readlines()
        commandStart=False
        for i in content:
            i=''.join([element.replace('\x1b','') for element in list(i)]).rstrip()
            if i.startswith(hostname):
                if 'temp' in locals():
                    log['sshCommand'].append(temp)
                temp={'command':'','response':[]}
                fullCommand=i[len(hostname)+1:]
                temp['command']=fullCommand
                temp['main_command']=fullCommand.split(' ')[0]
                commandStart=True
            elif commandStart:
                temp['response'].append(i)
        
    with open(store_path, 'a') as open_file:
        json.dump(log, open_file)
        open_file.write("\n")


def convertToText(logFile):
    os.system('./utils/vt100.py '+logFile+' > '+logFile+'.log')
    os.system('rm '+logFile)
    