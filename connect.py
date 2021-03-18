import win32file, win32pipe, socket, time, sys, _thread

if len(sys.argv) < 4:
    print("!!You need to give ip address, port and sleep timer separated with spaces in that order!!")
    sys.exit()
HOST, PORT, UPDATETIMER = sys.argv[1], sys.argv[2], int(sys.argv[3])

socket.setdefaulttimeout(10)
run = True

def request_loop(pipe):
    while run:
        readdata = win32file.ReadFile(pipe, 2048)
        sock.sendall(readdata[1])
        print("Sent " + str(sys.getsizeof(readdata[1])) + " bytes")
        writedata = sock.recv(2048)
        print("Received " + str(sys.getsizeof(writedata)) + " bytes")
        win32file.WriteFile(pipe, writedata)
        time.sleep(UPDATETIMER)

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
    pipe = create_winpipe()
    win32pipe.ConnectNamedPipe(pipe, None)
    print(">>got client, connecting")
    sock = socket.create_connection((HOST,PORT))
    print(">>connected, starting loop")
    _thread.start_new_thread(request_loop, (pipe,))
    input()
finally:
    win32file.CloseHandle(pipe)