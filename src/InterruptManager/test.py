if __name__ == "__main__":
    binary = '1111111111110000'
    decimal = int(binary, 2)
    if decimal > 32767:  # 如果解析出的数大于 32767（16位有符号数的最大值），则减去 65536
        decimal -= 65536

    print(decimal)  # 输出：-16

