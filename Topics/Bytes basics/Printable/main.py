char = int(input())

if 32 <= char <= 126:
    print(chr(char))
else:
    print(False)