package main 

import (
	"fmt"
)

func myXor(a,b int){
	fmt.Printf("XOR operation between %d (%04b) and %d (%04b) is %d (%04b)\n", a, a, b, b, a^b, a^b)
}

func myAND(a,b int){
	fmt.Printf("AND operation between %d (%04b) and %d (%04b) is %d (%04b)\n", a, a, b, b, a&b, a&b)
}

func myOR(a,b int){
	fmt.Printf("OR operation between %d (%04b) and %d (%04b) is %d (%04b)\n", a, a, b, b, a|b, a|b)
}

func myNOT(a,b int){
	fmt.Printf("NOT operation on %d (%04b) is %d (%04b)\n", a, a, ^a, ^a)
	fmt.Printf("NOT operation on %d (%04b) is %d (%04b)\n", b, b, ^b, ^b)
}

func main () {
	fmt.Println("Bitwise Operations Assignment Operations")
	var a,b int 
	fmt.Print("First Number:")
	fmt.Scanln(&a)
	fmt.Print("Second Number:")
	fmt.Scanln(&b)
	myXor(a,b)
	myNOT(a,b)
	myOR(a,b)
	myAND(a,b)
}