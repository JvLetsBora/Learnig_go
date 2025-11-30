



def main():
    for s in range(1, 10):
        for e in range(0, 10):
            for n in range(0, 10):
                for d in range(0, 10):
                    for m in range(1, 10):
                        for o in range(0, 10):
                            for r in range(0, 10):
                                for y in range(0, 10):
                                    if len(set([s, e, n, d, m, o, r, y])) == 8:
                                        send = s * 1000 + e * 100 + n * 10 + d
                                        more = m * 1000 + o * 100 + r * 10 + e
                                        money = m * 10000 + o * 1000 + n * 100 + e * 10 + y

                                        if send + more == money:
                                            print(f'{send} + {more} = {money}')


def moreEfective():
    valor1 = "send"
    valor2 = "more"
    result = "money"

    result = list(result)
    valor1 = list(valor1)
    valor2 = list(valor2)


    if len(valor1) < len(result) or len(valor2) < len(result):
        letters = [result[0], result[1]]
        result[0] = 1
        result[1] = 0

        n = 0
        for i in valor1:
            if letters[0] == i:
                valor1[n] = 1
            if letters[1] == i:
                valor1[n] = 0
            n += 1
        
        n = 0
        for i in valor2:
            if letters[0] == i:
                valor2[n] = 1
            if letters[1] == i:
                valor2[n] = 0
            n += 1

    print(f"{valor1} + {valor2} = {result}")

    s = 0
    e = 0
    n = 0
    d = 0

    r = 0
    e = 0

    y = 0


    valor1[-1] + valor2[-1] = result[-1]
    


if __name__ == '__main__':
    moreEfective()





    
    