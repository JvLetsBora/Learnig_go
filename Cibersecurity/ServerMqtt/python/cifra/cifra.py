alphabet = "abcdefghijklmnopqrstuvwxyz"

def cessar_cipher(data, key):
	result = ""
	chunck_count = 0
	_data = str(data)
		
	for i in range(len(_data)):
		c = _data[i] # Get the character
		if c != " ":
			is_upper = c.isupper()
			#print(c, " --> ", c.upper(), " ? ", c == c.upper())
			c = c.lower()
			index = alphabet.find(c)
			if index != -1:
				index = (index + key) % len(alphabet)
				c = alphabet[index]
				if is_upper:
					c = c.upper()
				key = (key + 1) % len(alphabet)
			
		elif c == " ":
			chunck_count += 2
			key = (key + chunck_count) % len(alphabet)
			#print("new key :",key, "chunck_count: ", chunck_count)
		
		result += c
	print("\n",result)

	return result.lower()

def decrypt_cessar_cipher(data, key): 
	result = ""
	chunck_count = 0
	_data = data
	for i in range(len(_data)):
		c = _data[i] # Get the character
		if c != " ":
			is_upper = c.isupper()
			
			c = c.lower()
			index = alphabet.find(c)
			if index != -1:
				index = (index + (len(alphabet) - key)) % len(alphabet)
				c = alphabet[index]
				if is_upper:
					c = c.upper()
				key = (key + 1) % len(alphabet)
		elif c == " ":
			chunck_count += 2
			key = (key + chunck_count) % len(alphabet)
		result += c
	print('\nDecrypted: ', result.lower())
	return result.lower()

# 26 - key

def shift_data(data, key):
	key = int(key)
	# Encryption
	strig_data = str(data)
	encrypted = cessar_cipher(strig_data, key)
	# Decryption
	decrypted = decrypt_cessar_cipher(encrypted, key)
	#Checks
	print(decrypted.lower() == strig_data.lower())


def main():
	input_data = input("Digite uma menssagem: ")
	key = input("Digite a chave: ")
	shift_data(input_data, key)

if __name__ == "__main__":
	main()