g = 5
p = 83

senha = 63
senha2 = 2

def main():
    lr = (g**senha)%83
    rl = (g**senha2)%83

    A = (rl**senha)%83
    B = (lr**senha2)%83

    # Então A e B são iguais
    print(A, B)


if __name__ == "__main__":
    main()