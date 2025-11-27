package crack

import (
	"fmt"
	"crypto/md5"
	"bufio"
	"strings"
	"os"
)

func CrackMD5(target, wordlist, verboseFile string) (string, int) {
	file, err := os.Open(wordlist)
	if err != nil {
		fmt.Println("Error opening wordlist:", err)
		return "", 0
	}
	defer file.Close()

	vf, err := os.Create(verboseFile)
	if err != nil {
		fmt.Println("Error creating verbose file:", err)
		return "", 0
	}
	defer vf.Close()
	scanner := bufio.NewScanner(file)
	attempts := 0
	for scanner.Scan() {
		pass := strings.TrimSpace(scanner.Text())
		if pass == "" {
			continue
		}
		attempts++
		hash := fmt.Sprintf("%x", md5.Sum([]byte(pass)))	
		
		line := fmt.Sprintf("password %d: %s -> %s", attempts, pass, hash)
		fmt.Println(line)
		vf.WriteString(line + "\n")

		// comparation 
		if hash == target {
			
			foundLine := fmt.Sprintf("Password FOUND '%s' Verbose saved to %s", pass, verboseFile)
			fmt.Println(foundLine)
			vf.WriteString(foundLine + "\n")
			return pass, attempts
		}
	}	

	notFoundLine := fmt.Sprintf("Password NOT FOUND Verbose saved to %s", verboseFile)
	fmt.Println(notFoundLine)
	vf.WriteString(notFoundLine + "\n")
	return "", attempts
}