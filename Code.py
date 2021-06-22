'''
Modified RSA algorithm =>
Sender side: 
	After encryption we 
		1. Set bits = [max(p, q) / min(p, q)]
		2. Modify each cipher in the cipher text by performing (cipher * bits) + abs(p - q)
		3. Perform right shift on the cipher text by 'bits' places.
Receiver side: 
	Before decryption we 
		1. Set bits = [max(p, q) / min(p, q)]
		2. Regain each cipher in the cipher text by performing (cipher - abs(p - q)) / bits
		3. Perform left shift on the cipher by 'bits' places.
'''

import math

# Checks if a number is prime or not
def isPrime(n):
	if (n < 2): 
		return False
	limit = int(math.sqrt(n))
	for i in range(2, limit+1):
		if n % i == 0:
			return False
	return True

# Calculates the GCD of two numbers 'a' and 'b'
def gcd(a, b):
	if (b == 0):
		return a
	return gcd(b, a % b)

# Calculates the GCD of two numbers 'a' and 'b'
# as well as coefficients 'x' and 'y' such that ax + by = GCD(a, b)
def egcd(a, b):
	if (b == 0):
		return [a, 1, 0]
	else:
		ans = egcd(b, a % b)
		temp = ans[1] - ans[2] * (a // b)
		ans[1] = ans[2]
		ans[2] = temp
		return ans

# Calculates the multiplicative inverse
def multiplicativeInverse(a, b):
	egcdArray = egcd(a, b)
	bMultiplier = egcdArray[2]

	if (bMultiplier < 0):
		return (bMultiplier % a + a) % a
	else:
		return (bMultiplier % a)

# Performs the exponentiation of large numbers (Binary Exponentiation)
def binaryPower(a, b, n):
	if (b == 0):
		return 1
	result = binaryPower(a, int(b / 2), n)

	# Odd power
	if (b % 2 == 1):
		return (result * result * a) % n
	# Even power
	else:
		return (result * result) % n

# Encrypts the plaintext (single integer)
def encrypt(M, e, n):
	C = binaryPower(M, e, n) % n
	# C = (M ** e) % n
	return C

# Decrypts the cipher text (single integer)
def decrypt(C, e, n):
	M = binaryPower(C, e, n) % n
	# M = (C ** e) % n
	return M

# Converts a string to list of corresponding numbers in Unicode
def stringToNumber(s):
	nums = []
	for i in s:
		if (i.isupper()):
			nums.append((ord(i) - 65 + 26))
		else:
			nums.append((ord(i) - 97))
	return nums

# Converts a list of numbers in Unicode to string
def numberToString(numList):
	s = ''
	for num in numList:
		if (num > 25):
			s += chr(num + 65 - 26)
		else:
			s += chr(num + 97)
	return s

## RSA Modification functions :  
# Performs right shift on the cipher text
# by a specified number of bits
def shiftRightCipher(cipherText, p, q):
	bits = math.ceil(max(p, q) / min(p, q))

	# Modify each cipher in the list
	for i in range(0, len(cipherText)):
		cipherText[i] = (cipherText[i] * bits) + abs(p - q) 

	# Shuffle the cipher array 
	shiftPoint = (bits) % len(cipherText)
	result = cipherText[shiftPoint : ] + cipherText[ : shiftPoint]
	return result

# Performs left shift on the cipher text
# by a specified number of bits
def shiftLeftCipher(cipherText, p, q):
	bits = math.ceil(max(p, q) / min(p, q))

	# Regain each cipher in the list
	for i in range(0, len(cipherText)):
		cipherText[i] = int((cipherText[i] - abs(p - q)) / bits)

	# Shuffle the array of ciphers
	shiftPoint = (len(cipherText) - bits) % len(cipherText)
	result = cipherText[shiftPoint : ] + cipherText[ : shiftPoint]
	return result

# Encrypts a string of characters
def encryptString(plainText, publicKey, p, q):
	cipherList = []
	# Converting plaintext(string) to numList(number)
	numList = stringToNumber(plainText)
	# print(f'Plain text in numbers = {numList}')
	
	for number in numList:
		# Plain text (M < n)
		M = number
		C = encrypt(M, publicKey[0], publicKey[1])
		cipherList.append(C)
	
	# Modifying cipherList
	print(f'RSA cipher => {cipherList}')
	modifiedCipher = shiftRightCipher(cipherList, p, q)
	print(f'Modified RSA cipher => {modifiedCipher}')
	return modifiedCipher
	
# Decrypts a string of characters
def decryptString(cipherText, privateKey, p, q):

	# Regaining the original cipher
	cipherList = shiftLeftCipher(cipherText, p, q)
	print(f'RSA cipher regained => {cipherList}')
	decryptList = []
	
	for cipher in cipherList:
		M = decrypt(cipher, privateKey[0], privateKey[1])
		decryptList.append(M)

	# print(f'decryptList = {decryptList}')
	# Converting decryptList(number) to decryptText(string)
	decryptText = numberToString(decryptList)
	return decryptText

# Performs initial RSA steps
def initializeRSA(p, q):

	# Calculation of n
	n = p * q
	print(f'n => {n}')

	# Calculation of phi(n)
	phi = (p - 1) * (q - 1)
	print(f'phi(n) => {phi}')

	# Select integer e such that gcd(phi, e) = 1
	for e in range(2, phi):
		if (gcd(phi, e) == 1):
			break
	print(f'e => {e}')

	# Calculaiton of d
	d = multiplicativeInverse(phi, e)
	print(f'd => {d}')

	# Public and private keys
	publicKey = [e, n]
	privateKey = [d, n]

	print(f'Public Key => {publicKey}')
	print(f'Private Key => {privateKey}')

	return publicKey, privateKey
	

if __name__ == '__main__':
	print()
	print('-------------------------')
	print('Modified RSA algorithm : ')
	print('-------------------------')
	p = int(input('Enter a prime number for p: '))
	while (not isPrime(p)):
		p = int(input('Please enter a prime number for p: '))
	
	q = int(input('Enter a prime number for q: '))
	while (not isPrime(q) or q == p):
		if (q == p):
			q = int(input('Please enter a number for q which is different from p: '))	
		else:
			q = int(input('Please enter a prime number for q: '))

	plainText = input('Please enter plain text \n(string of characters): ')

	print()
	print('-------------------------')
	print('Values of RSA variables : ')
	print('-------------------------')
	print(f'p => {p}')
	print(f'q => {q}')
	print(f'Plain text => {plainText}')

	publicKey, privateKey = initializeRSA(p, q)

	print()
	print('--------------------------')
	print('     Sender side')
	print('--------------------------')
	print('Encrypting...')

	cipher = encryptString(plainText, publicKey, p, q)
	print('Sending cipher...')
	
	print()

	print('--------------------------')
	print('     Receiver side')
	print('--------------------------')
	print(f'Cipher received => {cipher}')
	decryptedText = decryptString(cipher, privateKey, p, q)
	print('Decrypting...')
	print(f'Decrypted text : {decryptedText}')
