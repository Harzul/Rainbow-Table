from RainbowTable import Table,RT


def main():
    T = Table(5, 5, 5)
    T.generate_table()
    #print(T)
    T.w2file('test.txt')
    print(T(['2cac41f04fe3acec51f00bb2fb8d21bf','test.txt']))


if __name__ == "__main__":
    main()
