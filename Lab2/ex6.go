package main

import (
	"fmt"
)

func xorEncrypt(text string, key byte) string {
	result := make([]byte, len(text))
	for i := 0; i < len(text); i++ {
		result[i] = text[i] ^ key
	}
	return string(result)
}

func xorEncryptRepeating(text string, key string) string {
	if len(key) == 0 {
		return text
	}
	
	result := make([]byte, len(text))
	for i := 0; i < len(text); i++ {
		result[i] = text[i] ^ key[i%len(key)]
	}
	return string(result)
}

func toHex(s string) string {
	result := ""
	for i := 0; i < len(s); i++ {
		result += fmt.Sprintf("%02x ", s[i])
	}
	return result
}

func main() {
	var plaintext string
	var key byte
	
	fmt.Print("Enter plaintext message: ")
	fmt.Scanln(&plaintext)
	
	fmt.Print("Enter key (single character): ")
	var keyStr string
	fmt.Scanln(&keyStr)
	if len(keyStr) > 0 {
		key = keyStr[0]
	}
	
	fmt.Println("\n=== Results ===")
	fmt.Printf("Plaintext: %s\n", plaintext)
	fmt.Printf("Key: %c (0x%02x)\n", key, key)
	
	ciphertext := xorEncrypt(plaintext, key)
	fmt.Printf("\nCiphertext (hex): %s\n", toHex(ciphertext))
	
	decrypted := xorEncrypt(ciphertext, key)
	fmt.Printf("\nDecrypted: %s\n", decrypted)
}