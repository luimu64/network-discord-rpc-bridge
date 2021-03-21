import win32file, win32pipe, socket, sys, threading

#read ip address and port from config
try:
    config = open("config.txt")
except FileNotFoundError:
    print("config not found!")
    sys.exit()

#very complicated way of splitting the data twice and removing whitespaces
data = [i.split("=")[1].replace(" ", "") for i in config.read().split("\n")]
config.close()

try:
    HOST = data[0]
    PORT = data[1]
    VERBOSE = data[2] == "True" or False
except IndexError:
    print("something is wrong in your config")
    sys.exit()

socket.setdefaulttimeout(10)


def request_loop(pipe, sock):
    while True:
    
        #read what the client is sending into window's pipe
        try:
            readdata = win32file.ReadFile(pipe, 2048)
        except:
            print(">>client disconnected")
            return
            
        #send the data to socat if received
        if readdata[1] != None:
            sock.sendall(readdata[1])
            if VERBOSE:
                print(">>> " + readdata[1].decode("utf-8", "ignore") + "\n")
            else:
                print(">>> " + str(sys.getsizeof(readdata[1])) + " bytes")
            
        #receive response from socat
        try:
            writedata = sock.recv(2048)
        except:
            print(">>didn't receive data from host")
            
        #write the response to the pipe
        if writedata != None:
            win32file.WriteFile(pipe, writedata)
            if VERBOSE:
                print("<<< " + writedata.decode("utf-8", "ignore") + "\n")
            else:
                print("<<< " + str(sys.getsizeof(writedata)) + " bytes")


def create_winpipe():
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

def main():
    while True:
        #create pipe in windows
        pipe = create_winpipe()
        
        #wait until client(game) is started
        print(">>waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        
        print(">>got client, connecting to host")
        #connect to socat host
        try:
            sock = socket.create_connection((HOST,PORT))
        except (ConnectionRefusedError, socket.gaierror):
            print(">>couldn't connect to host, check config")
            sys.exit()
            
        print(">>connected, starting loop")
        
        #start the connection loop
        request_loop(pipe, sock)
        
        #close the windows pipe and socket so new ones can be created
        win32file.CloseHandle(pipe)
        sock.close()

if __name__ == "__main__":
    x = threading.Thread(target=main, daemon=True)
    x.start()
    input(">>Press any key to stop\n")