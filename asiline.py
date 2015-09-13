import sys

'''
If you're reading this, be aware that this is *not* the correct way to solve
problems like this. I just needed a quick and dirty hack. It will most probably
come back to bite me.

'''

'''
TODO: proper html, may need to use dict and uuids
      let user provide list of shell indicators
      change continues to returns by creating function
'''


def asi(fname, type="htmlbook"):

    in_code = False
    in_cont = False

    open_tag = "<screen>"
    close_tag = "</screen>"

    in_open_tag = "<userinput>"
    in_close_tag = "</userinput>"

    if type == "htmlbook":
        open_tag = '<pre data-type="programlisting">'
        close_tag = "</pre>"

        in_open_tag = "<strong>"
        in_close_tag = "</strong>"

    shell_indicators = set(["root@3baff51314d6:/data# ", "$ ",
                            "docker@etcd-1:~$ ", "docker@consul-1:~$ ",
                            "docker@overlay-1:~$ ", "docker@overlay-2:~$ "])
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
            # Also need to keep track of current input number and replace CO1. Sigh.
            ret = '<a class="co" id="co_' + filename + '_CO1-' + cur_anno + '" href="#callout_' + filename + '_CO1-' + cur_anno + '><img src="callouts/' + cur_anno + '.png" alt="' + cur_anno + '"></a>'
            cur_anno = ""
            return ret

        return ""


    def print_annos():
        for an in annos:
            print("Annotation ", an)

        annos.clear()

    def start_annos():
        if annos.size > 0:
            print('<dl class="calloutlist">')


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


                have_ind = ""
                for ind in shell_indicators:
                    if line.startswith(ind):
                        have_ind = ind

                if have_ind:
                    if line[-2:-1] == "\\":
                        print(have_ind, in_open_tag, line[len(have_ind):-1], anno(), sep='')
                        in_cont = True
                        continue
                    else:
                        print(have_ind, in_open_tag, line[len(have_ind):-1], in_close_tag, anno(), sep='')
                        continue

                print(line[:-1], anno(), sep='')
                continue

            else:
                #normal line, just to make sure isn't annotation explanation
                if line[0] == "<" and line[2] == ">":
                    if line[1] in annos:

                        an = line[1]

                        if an > 1:
                            print("</p></dd>")

                        print('<dt><a class="co" id="callout_' + filename + '_CO1-' + an + '" href="#co_' + filename + '_CO1-' + an + '"><img src="callouts/' + an + '.png" alt="' + an + '"></a></dt>'
                        print('<dd><p>', line[3:-1], sep='')

                        if last_anno:
                            print("</p></dd></dl>")
                        continue

                print(line, end='')

    if in_code:
        print("ERROR: unterminated asicode", file=sys.stderr)


if __name__ == "__main__":
    asi(sys.argv[1])
