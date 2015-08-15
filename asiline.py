import sys

'''
If you're reading this, be aware that this is *not* the correct way to solve
problems like this. I just needed a quick and dirty hack. It will most probably
come back to bite me.

'''

'''
TODO: handle annos
      when not in code
      check if line starts <x>
      if it does, look up corresponding annotation and substitute
      clear annos when hit code block
'''


def asi(fname, type="htmlbook"):

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

    cur_anno = ""

    annos = set([])


    #lines ending in an annotation
    def handle_annotation(line):
        nonlocal cur_anno
        if line[-2:-1] == ">" and line[-4:-3] == "<":
            cur_anno = line[-3:-2]
            annos.add(cur_anno)
            return line[:-4].rstrip() + "\n"

        return line


    def anno():
        nonlocal cur_anno
        if cur_anno:
            ret = "<callout " + cur_anno + "\>"
            cur_anno = ""
            return ret

        return ""


    def print_annos():
        for an in annos:
            print("Annotation ", an)

        annos.clear()


    with open(fname) as f:
        for line in f:

            #Check for opening/closing code
            if line[:4] == ",,,,":
                if not in_code:
                    print("++++")
                    print(open_tag)
                    annos.clear()
                    in_code = True
                    in_cont = False
                    continue
                else:
                    print(close_tag)
                    print("++++")
                    #print_annos()
                    in_code = False
                    in_cont = False
                    continue

            #handle code lines
            if in_code:

                line = handle_annotation(line)
                line = line.rstrip() + "\n"
                if in_cont:
                    if line[-2:-1] == "\\":
                        print(line[:-1], anno(), sep='')
                        continue
                    else:
                        print(line[:-1], in_close_tag, anno(), sep='')
                        in_cont = False
                        continue

                if line[:2] == "$ ":
                    if line[-2:-1] == "\\":
                        print("$ ", in_open_tag, line[2:-1], anno(), sep='')
                        in_cont = True
                        continue
                    else:
                        print("$ ", in_open_tag, line[2:-1], in_close_tag, anno(), sep='')
                        continue

                print(line[:-1], anno(), sep='')
                continue

            else:
                #normal line, just to make sure isn't annotation explanation
                if line[0] == "<" and line[2] == ">":
                    if line[1] in annos:
                        print('<annotation ref="', line[1], '"/>', line[3:-1], sep='')
                        continue

                print(line, end='')

    if in_code:
        print("ERROR: unterminated asicode", file=sys.stderr)


if __name__ == "__main__":
    asi(sys.argv[1])
