alphabet = "abcdefghijklmnopqrstuvwxyz"


codes = [ 
"DNWADFEFUD",
"MBSZDYQBKPSK",
"WLUZVSVNVLEPZAV",
"REQXFXVZEQXYXTLTDFE",
"JWXTYFMQYWOWHYGWMYOM",
"QNBETIOEVCQAIRBINIKIIL",
"ALCDELPQWAOLDDLTNHLALNVNIWQVNCDENLHVN",
"QWKQCEBUUCFUTHQTKHQJQDJERQJUQJUGKUVKHQ",
"TIXKLBLMXGVBTXHVTFBGAHWHXQBMHFTLTITVBXGVBTXHLXZKXWHWHXJNBEBUKBH",
"OBEBODBEPUFNQPRVFNBQSFOEFBWJWFSPQSFTFOUFFODPOUSBBWFSEBEFJSBMJCFSEBEF",
"WNEPMLXDHXZEPEDHEZREATDRXREOTLGEKVNHTZREKELYOYRXREEMXJXTLTDFTRXITVDXRX",
"NSBEPNQRHZEVBANBRFGNRZFHNIRYBPVQNQRZNFRZFHNQRGREZVANPNBQRFRETHVENQVNAGR",
"ZUMOSZFWYXOEMJZMWVTZWXVYZBWHMSEFZFWXZVWXVYZFWTWOXEJZSZMFWVWONYEOZFEZJTW",
"QUFGUCHKQUFCXKFCUCQKPGXKVCKUOCUGPHTGPVCNQUEQOEQTCIGOPQUVQTPCKPXGPEKXGKU",
"ELZTMEMZJTEEOJCEMZZFKOKAOEWKJETETEMJSJFJRMZZNFKNGTETOEUYTZFJKUEQAENMKFARGJLEME",
"EQJQRQDTYQPLOVQYEKPILQKRKVZIYTJQJPRQVQPGEVPAPVILQCTGZKVTQXIPAQFPQRPYQGPVFPLOVQJQ",
"ZBTQHNRHCZCDRNAQDZUHCZDLSNCNRNRRDTRZRODBSNRBNMSHMTZRDMCNRDFQDCNCNRFQZMCDRBQHZCNQDR",
"AHTDNEGCAEGXMTGUHVODNPPDOFOHDJFDPFNDRJSXEACTUFGOEBEXMVNDMBUSEMQLMQCFTPRRSJVLVPSXETWDSBEREYGUCFOQAWKGAECVPFUVOBUDETGXRFFRRQGOOMGJAEQGECQQDBFHQVGHLFFHIYCSASQIUUWUO",
"PDDPAIPDZGSDGZFSBSPDPDUPEKZGUGXKBKXSAGVBGABGNKSDGUXSZKSXGNSDOGZGDDGPBPADOXMSEPDUGDDPGUGDDPBPZXKDSVSKABSGYKSAGFGVGNKVKMZGUGSQGPSABGADGNKVUPXOXGADYPXZGXCKOGDKZXKGVSEGEKBPABXKOG",
"VRUVAEUSYMGYGSUINKAFRVKEZKGQVRYSMMVPRXFHZAUFFXRGPTUWZEJXVUHIZHVVZDKPNIRSZAVVBJLRYIYUHIGIMUOXRQRGVLGTRWJSVKUQCVVIILKVZICLJZYYNWGSOMTGVECMYIJIFPZQDBKWRSMIMLGHRMISKCXTBWVHZMDMFXVRXQG",
"MZNQXCVQKIATMGHHPQVPXVEMHNLIYKWAMVLZMDNMWQJEBSPFQTXGZZMTXQAZIRGJCMVGTVZALRLEQQWFVSXLMGXVXQVNVEZXIPBIYKQNIVLKWZIVPMVQXVZAUBFIYBWFWMQQKVXMDIJRWSCQICTVLKMYXFCIZNLTPYCRGEDKWAJYTABNLHTIZVTW"
]



def cessar_cipher(data, key):
	result = ""
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
		
		result += c
	print("\n",result)

	return result.lower()

def decrypt_caesar_cipher(data, key): 
    # Define o alfabeto usado na cifra
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    result = ""
    
    for c in data:  # Itera diretamente sobre cada caractere em 'data'
        if c.isalpha():  # Verifica se o caractere é uma letra
            is_upper = c.isupper()  # Verifica se é maiúsculo
            c = c.lower()  # Converte para minúsculo para o processamento
            
            # Calcula o índice da letra no alfabeto após a descriptografia
            index = alphabet.find(c)
            if index != -1:
                new_index = (index - key) % len(alphabet)  # Ajuste com mod para evitar erros de índice
                c = alphabet[new_index]  # Obtém a nova letra
                
                # Retorna à maiúscula, se necessário
                if is_upper:
                    c = c.upper()
        
        # Adiciona o caractere ao resultado (se não for letra, permanece igual)
        result += c
    
    print('\nDecrypted:', result)
    return result


# 26 - key

def shift_data(data, key):
	key = int(key)
	# Encryption
	strig_data = str(data)
	encrypted = cessar_cipher(strig_data, key)
	# Decryption
	decrypted = decrypt_caesar_cipher(encrypted, key)
	#Checks
	print(decrypted.lower() == strig_data.lower())


def main():
	# input_data = input("Digite uma menssagem: ")
	# key = input("Digite a chave: ")
	for i in codes:
		print("Descriptografando: ", i)
		for j in range(26):
			decrypt_caesar_cipher(i, j)

if __name__ == "__main__":
	# main()
	for i in codes:
		print("Descriptografando: ", i)
		for j in range(26):
			decrypt_caesar_cipher(i, j)