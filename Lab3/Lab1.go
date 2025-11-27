package main 

import (
	"fmt"
	"Week3/utils/crack"
)

func lab1(){
	var target, wordlist, verbose string
	fmt.Print("Lab 1: MD5 Cracker Program\n\n")
	fmt.Print("========MD5 Cracker Program========\n\n")
	target = "6a85dfd77d9cb35770c9dc6728d73d3f"
	wordlist = "nord_vpn.txt"
	verbose = "verbose_lab1.txt"

	password, attempts := crack.CrackMD5(target, wordlist, verbose)
	if password != "" {
		fmt.Printf("Password found: %s\n", password)
	} else {
		fmt.Printf("Password not found after %d attempts\n", attempts)
	}
}
