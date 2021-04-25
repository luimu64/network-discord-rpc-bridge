package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"

	"golang.org/x/sys/windows"
)

func check(err error) string {
	if err != nil {
		return "error"
	} else {
		return ""
	}
}

/*
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
*/

func create_pipe() windows.Handle {
	name, err := strconv.ParseUint("\\\\.\\pipe\\discord-ipc-0", 16, 16)
	check(err)
	name2 := uint16(name)
	var uname *uint16 = &name2
	pipe, err := windows.CreateNamedPipe(
		uname,
		windows.PIPE_ACCESS_DUPLEX|
			windows.PIPE_TYPE_BYTE|
			windows.PIPE_READMODE_BYTE,
		windows.PIPE_WAIT,
		1,
		2048,
		2048,
		0,
		nil)
	check(err)
	return pipe
}

func main() {
	data, err := ioutil.ReadFile("config.txt")
	if err != nil {
		fmt.Print(err)
	} else {
		rows := strings.Split(string(data), "\n")
		ip := strings.Split(rows[0], "=")[1]
		port := strings.Split(rows[1], "=")[1]
		verbose := strings.Split(rows[2], "=")[1]
		fmt.Print(ip + "\n" + port + "\n" + verbose + "\n")
	}
	create_pipe()
	fmt.Scanln()
}
