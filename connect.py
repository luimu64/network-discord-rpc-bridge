import win32file, win32pipe, socket, time, sys, _thread

if len(sys.argv) < 3:
    print("You need to give ip address and port separated with spaces in that order")
    sys.exit()

HOST, PORT, UPDATETIMER = sys.argv[1], sys.argv[2], 2

socket.setdefaulttimeout(10)


def request_loop(pipe):
    while True:
        try:
            #read what the client is sending into window's pipe
            readdata = win32file.ReadFile(pipe, 2048)
            #send the data to socat
            sock.sendall(readdata[1])
            print("Sent " + str(sys.getsizeof(readdata[1])) + " bytes")
        except:
            print(">>connection lost")
            sys.exit()
        try:
            #receive response from socat
            writedata = sock.recv(2048)
            #write the response to the pipe
            win32file.WriteFile(pipe, writedata)
            print("Wrote " + str(sys.getsizeof(writedata)) + " bytes")
        except:
            print(">>connection lost")
            sys.exit()

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

try:
    print(">>waiting for client")
    #create pipe in windows
    pipe = create_winpipe()
    #wait until client(game) is started
    win32pipe.ConnectNamedPipe(pipe, None)
    print(">>got client, connecting")
    #connect to socat host
    sock = socket.create_connection((HOST,PORT))
    print(">>connected, starting loop")
    #start the connection loop
    _thread.start_new_thread(request_loop, (pipe,))
    #ask for user input indefinitely to keep the script running
    input()
finally:
    win32file.CloseHandle(pipe)