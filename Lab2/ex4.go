package main 

import (
	"fmt"
)

func Add(a, b int) {
	fmt.Printf("Result: %d + %d = %d\n", a, b, a+b)
}

func Subtract(a, b int) {
	fmt.Printf("Result: %d - %d = %d\n", a, b, a-b)
}

func Multiply(a, b int) {
	fmt.Printf("Result: %d * %d = %d\n", a, b, a*b)
}	

func Divide(a, b int) {
	if b != 0 {
		fmt.Printf("Result: %d / %d = %d\n", a, b, a/b)
	} else {
		fmt.Println("Division by zero is not allowed.")
	}
}

func Modulo(a, b int) {
	if b != 0 {
		fmt.Printf("Result: %d %% %d = %d\n", a, b, a%b)
	} else {
		fmt.Println("Modulo by zero is not allowed.")
	}
}

func main () {
	var selection int
	for  {
	fmt.Println("\n===========Mini Calculator===========")
	fmt.Println("1.Add\n2.Subtract\n3.Multiply\n4.Divide\n5.Modulo\n6.Exit")
	fmt.Print("Select an operation (1-6): ")
	fmt.Scanln(&selection)
	switch selection {
	case 1:
		var a, b int
		fmt.Print("Enter a:")
		fmt.Scanln(&a)
		fmt.Print("Enter b:")
		fmt.Scanln(&b)
		Add(a, b)
	
	case 2:
		var a, b int
		fmt.Print("Enter a:")
		fmt.Scanln(&a)
		fmt.Print("Enter b:")
		fmt.Scanln(&b)
		Subtract(a, b)
	case 3:
		var a, b int
		fmt.Print("Enter a:")
		fmt.Scanln(&a)
		fmt.Print("Enter b:")
		fmt.Scanln(&b)
		Multiply(a, b)
	case 4:
		var a, b int
		fmt.Print("Enter a:")
		fmt.Scanln(&a)
		fmt.Print("Enter b:")
		fmt.Scanln(&b)
		Divide(a, b)
	case 5:
		var a, b int
		fmt.Print("Enter a:")
		fmt.Scanln(&a)
		fmt.Print("Enter b:")
		fmt.Scanln(&b)
		Modulo(a, b)
	case 6:
		fmt.Print("Exiting the calculator")
		return
	default:
		fmt.Println("Invalid selection. Please try again.")
	}
	}
}