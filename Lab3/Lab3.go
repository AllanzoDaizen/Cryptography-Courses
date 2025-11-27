package main 

import (
	"fmt"
	"Week3/utils/crack"
)

func lab3(){
	var target, wordlist, verbose string
	fmt.Print("Lab 3: SHA512 Cracker Program\n\n")
	fmt.Print("========SHA512 Cracker Program========\n\n")
	target = "485f5c36c6f8474f53a3b0e361369ee3e32ee0de2f368b87b847dd23cb284b316bb0f026ada27df76c31ae8fa8696708d14b4d8fa352dbd8a31991b90ca5dd38"
	wordlist = "nord_vpn.txt"
	verbose = "verbose_lab3.txt"

	password, attempts := crack.CrackSHA512(target, wordlist, verbose)
	if password != "" {
		fmt.Printf("Password found: %s\n", password)
	} else {
		fmt.Printf("Password not found after %d attempts\n", attempts)
	}
}
