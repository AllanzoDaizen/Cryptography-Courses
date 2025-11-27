package main

import (
    "bufio"
    "encoding/base64"
    "fmt"
    "os"
    "strings"
)

func toBinary(s string) string {
    binary := ""
    for i := 0; i < len(s); i++ {
        binary += fmt.Sprintf("%08b ", s[i])
    }
    return strings.TrimSpace(binary) 
}

func main() {
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("Enter a string: ")
    input, _ := reader.ReadString('\n')
    input = strings.TrimSpace(input)

    fmt.Println("Binary:", toBinary(input))
    fmt.Println("Hex:", fmt.Sprintf("%x", input))
    fmt.Println("Base64:", base64.StdEncoding.EncodeToString([]byte(input)))
}
