alphabet = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,    
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25


}

alphabet2 = {
    0: "z",
    1: "b",
    2: "c",
    3: "e",
    4: "d",
    5: "f",
    6: "g",
    7: "h",
    8: "i",
    9: "j",
    10: "k",
    11: "l",
    12: "m",
    13: "n",
    14: "p",
    15: "o",
    16: "q",
    17: "r",
    18: "s",
    19: "y",
    20: "u",
    21: "v",
    22: "w",
    23: "x",
    24: "t",
    25: "a"
}

# oi -> ff

def cipher(secret, alphabet):
    result = ""
    if len(alphabet) != 26:
        return "Alphabet must have 26 characters"

    for letter in secret:
        if letter != " ":
            index = alphabet[f'{letter.lower()}']
            result += alphabet2[index]
        else:
            result += " "
    
    return result

if __name__ == "__main__":
    print(cipher("Salve professor vamos ver se funciona", alphabet))
    print(cipher("Salve professor vamos ver se funciona", alphabet2))














