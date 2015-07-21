import sys


def ass(fname):

    in_code = False
    in_cont = False

    with open(fname) as f:
        for line in f:
            if line[:4] == ",,,,":
                if not in_code:
                    print("++++")
                    print("<screen>")
                    in_code = True
                    in_cont = False
                    continue
                else:
                    print("</screen>")
                    print("++++")
                    in_code = False
                    in_cont = False
                    continue

            if in_code and in_cont:
                if line[-2:-1] == "\\":
                    print(line, end='')
                    continue
                else:
                    print(line[2:-1], "</userinput>", sep='')
                    in_cont = False
                    continue

            if in_code and line[:2] == "$ ":
                if line[-2:-1] == "\\":
                    print("$ <userinput>", line[2:-1], sep='')
                    in_cont = True
                    continue
                else:
                    print("$ <userinput>", line[2:-1], "</userinput>", sep='')
                    continue
            else:
                print(line, end='')

    if in_code:
        print("ERROR: unterminated asscode", file=sys.stderr)


if __name__ == "__main__":
    ass(sys.argv[1])
