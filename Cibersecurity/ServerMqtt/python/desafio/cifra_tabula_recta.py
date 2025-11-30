tabula_recta = [
["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"],
["b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a"],
["c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b"],
["d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c"],
["e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d"],
["f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e"],
["g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f"],
["h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g"],
["i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h"],
["j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i"],
["k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j"],
["l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k"],
["m","n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l"],
["n","o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m"],
["o","p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n"],
["p","q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o"],
["q","r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p"],
["r","s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q"],
["s","t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r"],
["t","u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s"],
["u","v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t"],
["v","w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u"],
["w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v"],
["x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w"],
["y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x"],
["z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y"],
]

alphabet = "abcdefghijklmnopqrstuvwxyz"


# segredo // key - Coluna
# abcdefg // text - Linha
# sfiuiiu



def encrypt(text, key):
    result = ""
    if len(key) < len(text):
        return "Chave menor que o texto"
    
    for i in range(len(text)):
        column = alphabet.find(key[i])
        row = alphabet.find(text[i])
        result += tabula_recta[row][column]
            

    return result

def decrypt(encrypted_text, key):
    result = ""
    if len(key) < len(encrypted_text):
        return "Chave menor que o texto"
    
    for i in range(len(encrypted_text)):
        a = key[i].lower()
        column = alphabet.find(a)  # Localiza a coluna com base na chave
        # Percorre a linha da Tabula Recta na coluna correspondente para encontrar o índice do caractere criptografado
        for row in range(len(tabula_recta)):
            if tabula_recta[row][column] == encrypted_text[i]:
                result += alphabet[row]  # Adiciona a letra original ao resultado
                break

    return result

if __name__ == "__main__":
    text = "AFORCADEUMRIONAOESTAEMSUAVELOCIDADEMASEMSUADETERMINACAODESERGUIRADIANTE" # Coluna 
    key =  "ZUMOSZFWYXOEMJZMWVTZWXVYZBWHMSEFZFWXZVWXVYZFWTWOXEJZSZMFWVWONYEOZFEZJTW" # Linha
    
    print(encrypt(text, key))
    #print(decrypt(text, key))


# ZUMOSZFWYXOEMJZMWVTZWXVYZBWHMSEFZFWXZVWXVYZFWTWOXEJZSZMFWVWONYEOZFEZJTW
# AFORCADEUMRIONAOESTAEMSUAVELOCIDADEMASEMSUADETERMINACAODESERGUIRADIANTE