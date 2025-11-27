package main 

import (
	"fmt"
	"Week3/utils/crack"
)

func lab2(){
	var target, wordlist, verbose string
	fmt.Print("Lab 2: SHA1 Cracker Program\n\n")
	fmt.Print("========SHA1 Cracker Program========\n\n")
	target = "aa1c7d931cf140bb35a5a16adeb83a551649c3b9"
	wordlist = "nord_vpn.txt"
	verbose = "verbose_lab2.txt"

	password, attempts := crack.CrackSHA1(target, wordlist, verbose)
	if password != "" {
		fmt.Printf("Password found: %s\n", password)
	} else {
		fmt.Printf("Password not found after %d attempts\n", attempts)
	}
}
