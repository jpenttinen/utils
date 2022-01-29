package main

import (
	"fmt"
	"os"
)

func main() {

	if len(os.Args) != 3 {
		fmt.Println("Käyttö:", os.Args[0], "tunnit", "minuutit (sallittu arvo 1-59)")
		return
	}

	/* 	argsWithProg := os.Args
	   	argsWithoutProg := os.Args[1:]

	   	arg := os.Args[2]

	   	fmt.Println(argsWithProg)
	   	fmt.Println(argsWithoutProg)
	   	fmt.Println(arg)

	   	if 7%2 == 0 {
	   		fmt.Println("7 is even")
	   	} else {
	   		fmt.Println("7 is odd")
	   	}

	   	if 8%4 == 0 {
	   		fmt.Println("8 is divisible by 4")
	   	}

	   	if num := 9; num < 0 {
	   		fmt.Println(num, "is negative")
	   	} else if num < 10 {
	   		fmt.Println(num, "has 1 digit")
	   	} else {
	   		fmt.Println(num, "has multiple digits")
	   	} */
}
