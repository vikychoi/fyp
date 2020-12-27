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
                temp['command']=i
                commandStart=True
            elif commandStart:
                temp['response'].append(i)
        
    with open(store_path, 'a') as open_file:
        json.dump(log, open_file)
        open_file.write("\n")

def truncate_utf8_chars(filename, count, ignore_newlines=True):
    """
    Truncates last `count` characters of a text file encoded in UTF-8.
    :param filename: The path to the text file to read
    :param count: Number of UTF-8 characters to remove from the end of the file
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    """
    with open(filename, 'rb+') as f:
        last_char = None

        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1