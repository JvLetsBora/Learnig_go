from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad



class MyCrypto:
    def __init__(self):
        self.alphabet = {
            "a32": " ", "a33": "!", "a34": '"', "a35": "#", "a36": "$", "a37": "%", "a38": "&", "a39": "'", 
            "a40": "(", "a41": ")", "a42": "*", "a43": "+", "a44": ",", "a45": "-", "a46": ".", "a47": "/",
            "a48": "0", "a49": "1", "a50": "2", "a51": "3", "a52": "4", "a53": "5", "a54": "6", "a55": "7",
            "a56": "8", "a57": "9", "a58": ":", "a59": ";", "a60": "<", "a61": "=", "a62": ">", "a63": "?",
            "a64": "@", "a65": "A", "a66": "B", "a67": "C", "a68": "D", "a69": "E", "a70": "F", "a71": "G",
            "a72": "H", "a73": "I", "a74": "J", "a75": "K", "a76": "L", "a77": "M", "a78": "N", "a79": "O",
            "a80": "P", "a81": "Q", "a82": "R", "a83": "S", "a84": "T", "a85": "U", "a86": "V", "a87": "W",
            "a88": "X", "a89": "Y", "a90": "Z", "a91": "[", "a92": "\\", "a93": "]", "a94": "^", "a95": "_",
            "a96": "`", "a97": "a", "a98": "b", "a99": "c", "a100": "d", "a101": "e", "a102": "f", "a103": "g",
            "a104": "h", "a105": "i", "a106": "j", "a107": "k", "a108": "l", "a109": "m", "a110": "n", "a111": "o",
            "a112": "p", "a113": "q", "a114": "r", "a115": "s", "a116": "t", "a117": "u", "a118": "v", "a119": "w",
            "a120": "x", "a121": "y", "a122": "z", "a123": "{", "a124": "|", "a125": "}", "a126": "~"
        }

        self.latamAlphabet = {
            "a128": "À", "a129": "Á", "a130": "Â", "a131": "Ã", "a132": "Ä", "a135": "Ç", "a136": "È", 
            "a137": "É", "a138": "Ê", "a139": "Ë", "a141": "Í", "a145": "Ñ", "a146": "Ò", "a147": "Ó", 
            "a148": "Ô", "a149": "Õ", "a150": "Ö", "a153": "Ú", "a154": "Û", "a155": "Ü", "a157": "Ý",
            "a160": "à", "a161": "á", "a162": "â", "a163": "ã", "a164": "ä", "a167": "ç", "a168": "è",
            "a169": "é", "a170": "ê", "a171": "ë", "a173": "í", "a177": "ñ", "a178": "ò", "a179": "ó",
            "a180": "ô", "a181": "õ", "a182": "ö", "a185": "ú", "a186": "û", "a187": "ü", "a189": "ý",
            "a191": "ÿ"
        }

        self.padding = '|'
        self.is_padding = False
        self.key = "#$HGBHKMLO)(%pw2"
        self.iv = "1.&*!5079qwertyu"

    def utf8_to_str(self, data):
        result = ""
        for i, c in enumerate(data):
            if c == 124 and self.is_padding:
                continue
            elif c == 195:
                index = f"a{data[i + 1]}"
                if index in self.latamAlphabet:
                    result += self.latamAlphabet[index]
                else:
                    return "ERROR"
            elif c <= 128:
                index = f"a{c}"
                if index in self.alphabet:
                    result += self.alphabet[index]
                else:
                    return "ERROR"
        return result

    def encrypted(self, data: str) -> bytes:
        """
        Criptografa o texto usando AES CBC.
        :param data: String a ser criptografada.
        :return: Dados criptografados em bytes.
        """
        # Convertendo o texto para bytes
        data_bytes = data.encode('utf-8')
        # Aplicando padding para que o tamanho seja múltiplo de 16
        padded_data = pad(data_bytes, AES.block_size, style='pkcs7')
        # Criando o objeto AES com chave e IV
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # Criptografando os dados
        encrypted_data = cipher.encrypt(padded_data)
        return encrypted_data

    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Descriptografa os dados criptografados usando AES CBC.
        :param encrypted_data: Dados criptografados em bytes.
        :return: String descriptografada.
        """
        # Criando o objeto AES com chave e IV
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # Descriptografando os dados
        decrypted_data = cipher.decrypt(encrypted_data)
        # Removendo padding
        unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7')
        # Convertendo de volta para string
        return unpadded_data.decode('utf-8')


def main():
    # Criando uma instância de MyCrypto
    crypto = MyCrypto()

    # Texto original para encriptação
    original_text = "Olá, mundo! Isso é um teste com caracteres especiais: ÀÁÂÃÇÉ."
    print(f"Texto original: {original_text}")

    # Simulando encriptação
    print("\n--- Início da encriptação ---")
    encrypted_data = crypto.encrypted(original_text)
    print(f"Texto encriptado (em bytes): {encrypted_data}")

    # Simulando descriptografia
    print("\n--- Início da descriptografia ---")
    decrypted_text = crypto.decrypt(encrypted_data)
    print(f"Texto descriptografado: {decrypted_text}")

    # Verificando se o texto original é igual ao texto descriptografado
    if original_text == decrypted_text:
        print("\nSucesso! O texto descriptografado é igual ao original.")
    else:
        print("\nErro! O texto descriptografado não é igual ao original.")

    # Testando o método utf8_to_str com dados UTF-8
    print("\n--- Testando a conversão UTF-8 para string ---")
    utf8_data = original_text.encode('utf-8')  # Converte texto para bytes UTF-8
    print(f"Dados UTF-8: {utf8_data}")
    converted_text = crypto.utf8_to_str(utf8_data)
    print(f"Texto convertido: {converted_text}")


if __name__ == "__main__":
    main()
