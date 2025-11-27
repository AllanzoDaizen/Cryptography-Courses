package main

import (
	"fmt"
)

func main() {
	fmt.Println("Logical Operations")
	var a,b int 
	fmt.Print("First Number:")
	fmt.Scanln(&a)
	fmt.Print("Second Number:")
	fmt.Scanln(&b)

	positive := (a > 0) && (b > 0)
	fmt.Println("Both numbers are positive:", positive)

	oneGreater := (a > b) || (b > a)
	fmt.Println("At least one number is greater:", oneGreater)

	notEqual := (a != b)
	fmt.Println("Both numbers are not equal:", notEqual)

}