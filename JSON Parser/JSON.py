try:
    n = input()
    column = ""
    flag = 0
    i = 0
    c1in = 0
    c1out = 0
    c2in = 0
    c2out = 0
    while i < len(n):
        if n[i] == " ":
            i += 1
            continue
        if (n[i]    == "[" or n[i] == "{") and (n[i + 1] != "]" and n[i + 1] != "}"):
            if n[i] == "[":
                c1in += 1
            else:
                c2in += 1
            column += "  "
            i += 1
        elif (n[i] == "[" or n[i] == "{") and (n[i + 1] == "]" or n[i + 1] == "}"):
            i += 2
        elif n[i] == ",":
            while n[i+1]==" ":
                i+=1
            if n[i+1]=="]" or n[i+1]=="}":
                flag=1
            i += 1
        elif n[i] == "]" or n[i] == "}":
            if n[i] == "]":
                c1out += 1
            else:
                c2out += 1
            column = column.replace(" ", "", 2)
            i += 1
        elif n[i] == '"':
            t = 0
            i += 1
            while n[i + t] != '"':
                t += 1
            i += t + 1
            if i >= len(n):
                i += 1
                continue
            if n[i] == ":":
                i += 1
        elif n[i] in "-0123456789.":
            p = 0
            while n[i + p] in "-0123456789.":
                p += 1
            i += p
        elif n[i] == "f":
            if n[i + 1] == "a" and n[i + 2] == "l" and n[i + 3] == "s" and n[i + 4] == "e":
                i += 5
            else:
                flag = 1
        elif n[i] == "t" and n[i + 1] == "r" and n[i + 2] == "u" and n[i + 3] == "e":
            i += 4
        elif n[i] == "n" and n[i + 1] == "u" and n[i + 2] == "l" and n[i + 3] == "l":
            i += 4
        else:
            flag = 1
            break
    if c1in != c1out or c2in != c2out:
        flag = 1
    if flag == 1:
        print("---")
    else:
        column = ""
        flag = 0
        i = 0
        while i < len(n):
            if n[i] == " ":
                i += 1
                continue
            if (n[i] == "[" or n[i] == "{") and (n[i + 1] != "]" and n[i + 1] != "}"):
                print(n[i])
                column += "  "
                i += 1
                print(column, end="")
            elif (n[i] == "[" or n[i] == "{") and (n[i + 1] == "]" or n[i + 1] == "}"):
                print(n[i], end="")
                print(n[i + 1], end="")
                i += 2
            elif n[i] == ",":
                print(n[i])
                print(column, end="")
                i += 1
            elif n[i] == "]" or n[i] == "}":
                print()
                column = column.replace(" ", "", 2)
                print(column, end="")
                print(n[i], end="")
                i += 1
            elif n[i] == '"':
                print('"', end="")
                t = 0
                i += 1
                while n[i + t] != '"':
                    print(n[i + t], end="")
                    t += 1
                print(n[i + t], end="")
                i += t + 1
                if i >= len(n):
                    i += 1
                    continue
                if n[i] == ":":
                    print(": ", end="")
                    i += 1
            elif n[i] in "-0123456789.":
                p = 0
                while n[i + p] in "-0123456789.":
                    print(n[i + p], end="")
                    p += 1
                i += p
            elif n[i] == "f":
                print("False", end="")
                i += 5
            elif n[i] == "t":
                print("True", end="")
                i += 4
            elif n[i] == "n":
                print("None", end="")
                i += 4
            else:
                flag = 1
except:
    print("---")