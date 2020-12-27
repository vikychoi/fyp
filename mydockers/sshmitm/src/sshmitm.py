
from binascii import hexlify
import threading
import traceback
import socketserver
import logging
import paramiko
from paramiko.py3compat import u
import select
import time
import re
import os 
from utils.utils import truncate_utf8_chars
from utils.utils import logToJson

PORT = 3000
REMOTE_PORT = 22
#LOG_FILE_LOGIN='log/sshLogin.log'
DENY_ALL = False
DOMAIN = "sshd"
HOSTNAME="#"
# setup logging
def getLogger(name,log_file):
    logger = logging.getLogger(name+".log")
    logger.setLevel(logging.INFO)
    lh = logging.FileHandler(log_file)
    lh.terminator = ""
    logger.addHandler(lh)
    return logger,lh

#logger_login,_ = getLogger("login",LOG_FILE_LOGIN)


def ttyDecode(byteChar,log_file):
    strByte=str(byteChar)
    if strByte=="b'\\x08\\x1b[J'": #backspace
        truncate_utf8_chars(log_file, 1, ignore_newlines=True)
        return ""
    string=byteChar.decode()
    # ansi_escape = re.compile(r'''
    #     \x1B  # ESC
    #     (?:   # 7-bit C1 Fe (except CSI)
    #         [@-Z\\-_]
    #     |     # or [ for CSI, followed by a control sequence
    #         \[
    #         [0-?]*  # Parameter bytes
    #         [ -/]*  # Intermediate bytes
    #         [@-~]   # Final byte
    #     )
    # ''', re.VERBOSE)
    #print(string)

    badCharacter=['\[[0-9][a-z]','\[[0-9];[0-9][0-9][a-z]','\[[a-z]']
    for regex in badCharacter:
        ansi_escape=re.compile(regex)
        if ansi_escape.search(string):
            string = ansi_escape.sub('', string)
    return string


host_key = paramiko.RSAKey(filename='test_rsa.key')

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
        self.accessTime=time.strftime('%Y%m%d-%H%M%S',time.localtime())
        if DENY_ALL is True:
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
                logToJson(HOSTNAME,server.username,server.password,server.accessTime,server.client_address[0],'auth_failed')
                print('Authentication failed')
                return
            
            print('Authenticated!')
            chan2 = self.client.invoke_shell()

            self.LOG_FILE_SERVER = 'log/sshmitm-'+server.accessTime+'.log'
            self.logger_server,self.lh=getLogger("server",self.LOG_FILE_SERVER)
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
                    self.logger_server.info('%s' % ttyDecode(x,self.LOG_FILE_SERVER))
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
                self.logger_server.removeHandler(self.lh)

                logToJson(HOSTNAME,server.username,server.password,
                            server.accessTime,server.client_address[0],
                            'logged_in',self.LOG_FILE_SERVER)
            except:
                pass


if __name__=="__main__":
    sshserver = socketserver.ThreadingTCPServer(("0.0.0.0", PORT), SSHHandler)
    sshserver.serve_forever()
