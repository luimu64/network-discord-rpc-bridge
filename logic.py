import win32file
import win32pipe
import socket
import sys
import configparser


class connection_manager:
    def __init__(self):
        self.running = True
        socket.setdefaulttimeout(10)
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            self.HOST = config['OPTIONS']['HostIpAddress']
            self.PORT = config['OPTIONS']['HostPort']
            self.VERBOSE = config.getboolean('OPTIONS', 'VerboseOutput')
        except IndexError:
            print("[error] something is wrong in your config")
            sys.exit()

    def request_loop(self, pipe, sock):
        while True:
            # read what the client is sending into window's pipe
            try:
                readdata = win32file.ReadFile(pipe, 2048)
            except:
                print("[info] client disconnected")
                return

            # send the data to socat if received
            if readdata[1] != None:
                sock.sendall(readdata[1])
                if self.VERBOSE:
                    print(
                        ">>> " + readdata[1].decode("utf-8", "ignore") + "\n")
                else:
                    print(">>> " + str(sys.getsizeof(readdata[1])) + " bytes")

            # receive response from socat
            try:
                writedata = sock.recv(2048)
                win32file.WriteFile(pipe, writedata)
                if self.VERBOSE:
                    print("<<< " + writedata.decode("utf-8", "ignore") + "\n")
                else:
                    print("<<< " + str(sys.getsizeof(writedata)) + " bytes")
            except:
                print("[error] didn't receive data from host")

    def create_winpipe(self):
        pipe = win32pipe.CreateNamedPipe(
            r'\\.\pipe\discord-ipc-0',
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_BYTE |
            win32pipe.PIPE_READMODE_BYTE |
            win32pipe.PIPE_WAIT,
            1,
            2048,
            2048,
            0,
            None)
        return pipe

    def main(self):
        print("[info] main loop started")
        while self.running:
            # create pipe in windows
            pipe = self.create_winpipe()

            # wait until client(game) is started
            print("[info] waiting for client")
            win32pipe.ConnectNamedPipe(pipe, None)

            print("[info] got client, connecting to host")
            # connect to socat host
            try:
                sock = socket.create_connection((self.HOST, self.PORT))
            except (ConnectionRefusedError, socket.gaierror):
                print("[error] couldn't connect to host, check config")
                sys.exit()

            print("[info] connected, starting loop")

            # start the connection loop
            self.request_loop(pipe, sock)

            # close the windows pipe and socket so new ones can be created
            win32file.CloseHandle(pipe)
            sock.close()
