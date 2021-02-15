
from binascii import hexlify
import threading
import traceback
import socketserver
import paramiko
from paramiko.py3compat import u
import select
import time
from datetime import datetime
import re
import os 
from utils.utils import logToJson
from utils.utils import convertToText
import urllib.request

PORT = 3000
REMOTE_PORT = 22
DENY_ALL = False
DOMAIN = "sshd"
HOSTNAME="#"

host_key = paramiko.RSAKey(filename='test_rsa.key')
HOST_IP=urllib.request.urlopen('https://ident.me').read().decode('utf8')
print('Read key: ' + u(hexlify(host_key.get_fingerprint())))


class Server (paramiko.ServerInterface):

    def __init__(self, client_address):
        self.event = threading.Event()
        self.client_address = client_address
           

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
#        logger_login.info('IP: %s, User: %s, Password: %s, Time : %s \r\n' % (self.client_address[0],
#                                                        username, password,time.strftime('%Y%m%d-%H%M%S',
#                                                        time.localtime())))                                                
        self.password = password
        self.username = username
        self.accessTime=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if DENY_ALL is True:
            return paramiko.AUTH_FAILED

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(DOMAIN, username=username,password=password, port=REMOTE_PORT)
        except paramiko.ssh_exception.AuthenticationException:
            logToJson(HOSTNAME,self.username,self.password,self.accessTime,self.client_address[0],HOST_IP,'auth_failed')
            print('client to sshmitm Authentication failed')
            return paramiko.AUTH_FAILED
        
        return paramiko.AUTH_SUCCESSFUL


    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        return True


class SSHHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            t = paramiko.Transport(self.connection)
            t.local_version="SSH-2.0-OpenSSH_8.4"
            t.add_server_key(host_key)
            server = Server(self.client_address)
            try:
                t.start_server(server=server)
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
                return

            # wait for auth
            chan = t.accept(20)
            if chan is None:
                t.close()
                return

            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self.client.connect(DOMAIN, username=server.username,
                                    password=server.password, port=REMOTE_PORT)
            except paramiko.ssh_exception.AuthenticationException:
                #logToJson(HOSTNAME,server.username,server.password,server.accessTime,server.client_address[0],'auth_failed')
                #print('Authentication failed')
                print('sshmitm to sshd Authentication failed')
                return
            
            print('Authenticated!')
            chan2 = self.client.invoke_shell()

            self.LOG_FILE = 'log/sshmitm-'+server.accessTime
            logFile = open(self.LOG_FILE, 'ab')

            while True:
                r, w, e = select.select([chan2, chan], [], [])
                if chan in r:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        break
                    chan2.send(x)

                if chan2 in r:
                    x = chan2.recv(1024)
                    if len(x) == 0:
                        break
                    logFile.write(x)
                    chan.send(x)

            server.event.wait(10)
            if not server.event.is_set():
                print('*** Client never asked for a shell.')
                t.close()
                return
            print(server.get_allowed_auths)
            chan.close()

        except Exception as e:
            print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
            traceback.print_exc()
        finally:
            try:
                t.close()
                logFile.close()
                convertToText(self.LOG_FILE)
                logToJson(HOSTNAME,server.username,server.password,
                            server.accessTime,server.client_address[0],
                            'logged_in',HOST_IP,self.LOG_FILE+'.log')
            except:
                pass


if __name__=="__main__":
    sshserver = socketserver.ThreadingTCPServer(("0.0.0.0", PORT), SSHHandler)
    sshserver.serve_forever()
