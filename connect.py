import win32file, win32pipe, socket, sys, threading

if len(sys.argv) < 3:
    print("You need to give ip address and port separated with spaces in that order")
    sys.exit()

HOST, PORT, UPDATETIMER = sys.argv[1], sys.argv[2], 2

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
            print("Sent " + str(sys.getsizeof(readdata[1])) + " bytes")
            
        #receive response from socat
        try:
            writedata = sock.recv(2048)
        except:
            print(">>didn't receive data from host")
            
        #write the response to the pipe
        if writedata != None:
            win32file.WriteFile(pipe, writedata)
            print("Wrote " + str(sys.getsizeof(writedata)) + " bytes")


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
        except ConnectionRefusedError:
            print(">>couldn't connect to host, check ip and port")
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