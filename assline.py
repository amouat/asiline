import sys


def ass(fname, type="docbook"):

    in_code = False
    in_cont = False

    open_tag = "<screen>"
    close_tag = "</screen>"

    in_open_tag = "<userinput>"
    in_close_tag = "</userinput>"

    if type == "htmlbook":
        open_tag = "<pre>"
        close_tag = "</pre>"

        in_open_tag = "<strong>"
        in_close_tag = "</strong>"

    with open(fname) as f:
        for line in f:
            if line[:4] == ",,,,":
                if not in_code:
                    print("++++")
                    print(open_tag)
                    in_code = True
                    in_cont = False
                    continue
                else:
                    print(close_tag)
                    print("++++")
                    in_code = False
                    in_cont = False
                    continue

            if in_code and in_cont:
                if line[-2:-1] == "\\":
                    print(line, end='')
                    continue
                else:
                    print(line[2:-1], in_close_tag, sep='')
                    in_cont = False
                    continue

            if in_code and line[:2] == "$ ":
                if line[-2:-1] == "\\":
                    print("$ ", in_open_tag, line[2:-1], sep='')
                    in_cont = True
                    continue
                else:
                    print("$ ", in_open_tag, line[2:-1], in_close_tag, sep='')
                    continue
            else:
                print(line, end='')

    if in_code:
        print("ERROR: unterminated asscode", file=sys.stderr)


if __name__ == "__main__":
    ass(sys.argv[1])
