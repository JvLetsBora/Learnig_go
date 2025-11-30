valor1 = "one"
valor2 = 'two'
# one + one = two

def main():
    for o in range(1, 10):
        for n in range(0, 10):
            for e in range(0, 10):
                for t in range(1, 10):
                    for w in range(0, 10):
                        if len(set([o, n, e])) == 3:
                            one = o * 100 + n * 10 + e
                            two = t * 100 + w * 10 + o

                            if one + one == two:
                                print(f'{one} + {one} = {two}')
                                return
    
    print("No solution")




if __name__ == '__main__':
    main()