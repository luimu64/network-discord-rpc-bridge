package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

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
}
