package main

import (
    "crypto/md5"
    "crypto/sha1"
    "crypto/sha256"
    "crypto/sha512"
    "crypto/sha3"
    "fmt"
)

func lab0(){
    var input1, input2 string

	fmt.Print("Lab 0: Proof the Hash Program\n\n")
	fmt.Print("========Name + Hashing Program========\n\n")
    fmt.Print("Please input value 1: ")
    fmt.Scan(&input1)
    fmt.Print("\nPlease input value 2: ")
    fmt.Scan(&input2)

    proofMe(input1, input2)
}

func proofMe(txt1, txt2 string) {
    
    hashMD5_A := fmt.Sprintf("%x", md5.Sum([]byte(txt1)))
    hashMD5_B := fmt.Sprintf("%x", md5.Sum([]byte(txt2)))
    printResult("MD5", hashMD5_A, hashMD5_B)


    hashSHA1_A := fmt.Sprintf("%x", sha1.Sum([]byte(txt1)))
    hashSHA1_B := fmt.Sprintf("%x", sha1.Sum([]byte(txt2)))
    printResult("SHA1", hashSHA1_A, hashSHA1_B)


    hashSHA256_A := fmt.Sprintf("%x", sha256.Sum256([]byte(txt1)))
    hashSHA256_B := fmt.Sprintf("%x", sha256.Sum256([]byte(txt2)))
    printResult("SHA256", hashSHA256_A, hashSHA256_B)

  
    hashSHA512_A := fmt.Sprintf("%x", sha512.Sum512([]byte(txt1)))
    hashSHA512_B := fmt.Sprintf("%x", sha512.Sum512([]byte(txt2)))
    printResult("SHA512", hashSHA512_A, hashSHA512_B)

 
    hashSHA3_A := fmt.Sprintf("%x", sha3.Sum256([]byte(txt1)))
    hashSHA3_B := fmt.Sprintf("%x", sha3.Sum256([]byte(txt2)))
    printResult("SHA3-256", hashSHA3_A, hashSHA3_B)
}

func printResult(algorithm, hashA, hashB string) {
    match := "No Match!"
    if hashA == hashB {
        match = "Match!"
    }

    fmt.Printf("\nHash (%s):\n", algorithm)
    fmt.Println("Output A : ", hashA)
    fmt.Println("Output B : ", hashB)
    fmt.Println("=>", match)
}
