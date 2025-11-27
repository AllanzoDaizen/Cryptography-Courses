package main

import (
	"fmt"
)

func main() {
	for {
		fmt.Println()
		fmt.Println("Choose exercise to run: ")
		fmt.Println("1. lab0 - Proof the Hash Program")
		fmt.Println("2. lab1 - Made the Password Cracking (MD5)")
		fmt.Println("3. lab2 - Made the Password Cracking (SHA1)")
		fmt.Println("4. lab3 - Made the Password Cracking (SHA512)")
		fmt.Println("5. Exit program")
		fmt.Print("Enter choice: ")

		var choice int
		_, err := fmt.Scan(&choice)
		if err != nil {
			// Clear the input buffer
			var discard string
			fmt.Scanln(&discard)
			fmt.Println("Invalid input. Please enter a number (1-5).")
			continue
		}

		switch choice {
		case 1:
			lab0()
		case 2:
			lab1()
		case 3:
			lab2()
		case 4:
			lab3()
		case 5:
			fmt.Println("Exiting. Bye!")
			return
		default:
			fmt.Println("Unknown choice. Please enter 1-5.")
		}
	}
}