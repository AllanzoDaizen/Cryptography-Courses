package main

import (
	"fmt"
)

func main(){
	fmt.Println("Assignment Operations")
	var a int
	var b int
	fmt.Print("First Number:")
	fmt.Scanln(&a)
	fmt.Print("Second Number:")
	fmt.Scanln(&b)
	fmt.Println(a,"=",b )
	fmt.Println(a,"+=",b,"is", a+b)
	fmt.Println(a,"-=",b,"is", a-b)
	fmt.Println(a,"*=",b,"is",a*b)
	if b != 0 {
		fmt.Println(a,"/=",b,"is", a/b)
	}else{
		fmt.Println("Division by zero is not allowed.")
	}

	if b != 0 {
		fmt.Println(a,"%=",b,"is", a%b)
	}else{
		fmt.Println("Modulo by zero is not allowed.")
	}
}