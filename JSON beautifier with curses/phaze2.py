import curses
def printonterm(n,scr):
    column= ""
    curser_y=0
    i=0
    re=""
    while i < len(n):
        if n[i] == " ":
            i += 1
            continue
        if (n[i] == "[" or n[i] == "{") and (n[i + 1] != "]" and n[i + 1] != "}"):
            scr.addstr(n[i])
            curser_y+=1
            scr.move(curser_y,0)
            column += "  "
            scr.addstr(column)
            re += n[i] + "/" + column
            i += 1
        elif (n[i] == "[" or n[i] == "{") and (n[i + 1] == "]" or n[i + 1] == "}"):
            scr.addstr(n[i])
            scr.addstr(n[i+1])
            re += n[i] + n[i + 1]
            i += 2
        elif n[i] == ",":
            scr.addstr(n[i])
            curser_y += 1
            scr.move(curser_y, 0)
            scr.addstr(column)
            re += n[i] + "/" + column
            i += 1
        elif n[i] == "]" or n[i] == "}":
            curser_y += 1
            scr.move(curser_y, 0)
            column = column.replace(" ", "", 2)
            scr.addstr(column)
            scr.addstr(n[i])
            re += "/" + column + n[i]
            i += 1
        elif n[i] == '"':
            scr.addstr(n[i])
            t = 0
            re += n[i]
            i += 1
            while n[i + t] != '"':
                scr.addstr(n[i+t])
                re += n[i + t]
                t += 1
            re += n[i + t]
            scr.addstr(n[i+t])
            i += t + 1
            if i >= len(n):
                i += 1
                continue
            if n[i] == ":":
                scr.addstr(n[i])
                re += ":"
                i += 1
        elif n[i] in "-0123456789.":
            p = 0
            while n[i + p] in "-0123456789.":
                scr.addstr(n[i+p])
                re += n[i + p]
                p += 1
            i += p
        elif n[i] == "f":
            scr.addstr("False")
            re += "False"
            i += 5
        elif n[i] == "t":
            scr.addstr("True")
            re += "True"
            i += 4
        elif n[i] == "n":
            scr.addstr("None")
            re += "None"
            i += 4
    return re

def secoundrybeautifier(data,scr):
    i=0
    scr.clear()
    newstring=""
    while i<len(data):
        if data[i]=="/":
            newstring+="\n"
        else:
            newstring+=data[i]
        i+=1
    scr.addstr(newstring)

def gonear(line,data):
    j,i=0,1
    while i!=line:
        j+=1
        if data[j]=="/":
            i+=1
    j+=1
    p=0
    while data[j+p]==" ":
        p+=1
    return (p,p+j)

def save(data):
    i,saved=0,[]
    while i<len(data):
        if data[i]=="[" and data[i+1]!="]":
            c=1
            j=0
            s="["
            while c!=0:
                j+=1
                if data[i+j]=="[":
                    c+=1
                elif data[i+j]=="]":
                    c-=1
                s+=data[i+j]
            saved.extend([[1,s]])
        elif data[i]=="{" and data[i+1]!="}":
            c=1
            j=0
            s="{"
            while c!=0:
                j+=1
                if data[i+j]=="{":
                    c+=1
                elif data[i+j]=="}":
                    c-=1
                s+=data[i+j]
            saved.extend([[1,s]])
        i+=1
    return saved

def printme(saved,scr):
    i=0
    re=""
    counter = -1
    while i<len(saved[0][1]):
        if (saved[0][1][i]=="[" and saved[0][1][i+1]!="]"):
            counter+=1
            if saved[counter][0]==0:
                re += "[...]"
                c = 1
                while c != 0:
                    i += 1
                    if saved[0][1][i] == "[":
                        c += 1
                    elif saved[0][1][i] == "]":
                        c -= 1
            else:
                re += saved[0][1][i]
        elif (saved[0][1][i]=="{" and saved[0][1][i+1]!="}"):
            counter += 1
            if saved[counter][0] == 0:
                re += "{...}"
                c = 1
                while c != 0:
                    i += 1
                    if saved[0][1][i] == "{":
                        c += 1
                    elif saved[0][1][i] == "}":
                        c -= 1
            else:
                re += saved[0][1][i]
        else:
            re+=saved[0][1][i]
        i+=1
    secoundrybeautifier(re,scr)
    return re

def main(data):
    scr = curses.initscr()
    scr.keypad(True)
    curses.noecho()
    data=printonterm(data,scr)
    saved=save(data)
    curses.curs_set(2)
    scr.move(0,0)
    curser_y,curser_x,line=0,0,1
    while True:
        c=scr.getch()
        try:
            if c==27:
                break
            elif c==258: #down
                curser_y+=1
                line+=1
                curser_x,o=gonear(line,data)
            elif c==259: #up
                curser_y-=1
                line-=1
                curser_x,o=gonear(line,data)
            elif c==260: #left
                o,where=gonear(line, data)
                if where==1:
                    where=0
                if data[where]=="[" and data[where+1]!="]" and data[where+1]!=".":
                    i,counter=0,-1
                    newstate=""
                    while i<len(data):
                        if (data[i]=="[" and data[i+1]!="]") or (data[i]=="{" and data[i+1]!="}") and i<=where:
                            counter+=1
                        newstate+=data[i]
                        if i==where:
                            newstate+="...]"
                            t=1
                            while t!=0:
                                i+=1
                                if data[i]=="[":
                                    t+=1
                                elif data[i]=="]":
                                    t-=1
                        i+=1
                    saved[counter][0]=0
                    data=newstate
                    secoundrybeautifier(data,scr)
                elif data[where]=="{" and data[where+1]!="}" and data[where+1]!=".":
                    i,counter=0,-1
                    newstate = ""
                    while i < len(data):
                        if (data[i]=="[" and data[i+1]!="]") or (data[i]=="{" and data[i+1]!="}") and i<=where:
                            counter+=1
                        newstate += data[i]
                        if i == where:
                            newstate += "...}"
                            t = 1
                            while t != 0:
                                i += 1
                                if data[i] == "{":
                                    t += 1
                                elif data[i] == "}":
                                    t -= 1
                        i += 1
                    saved[counter][0] = 0
                    data = newstate
                    secoundrybeautifier(data, scr)
                else:
                    t=1
                    k=0
                    while t!=0:
                        k+=1
                        if data[where-k]=="[" or data[where-k]=="{":
                            t-=1
                        elif data[where-k]=="]" or data[where-k]=="}":
                            t+=1
                        elif data[where-k]=="/":
                            curser_y-=1
                            line-=1
                    curser_x,o=gonear(line,data)
            elif c==261: #right
                o, where = gonear(line, data)
                if where==1:
                    where=0
                if data[where] == "[" and data[where+1]==".":
                    i,counter=0,-1
                    while i<=where:
                        if (data[i]=="[" and data[i+1]!="]") or (data[i]=="{" and data[i+1]!="}"):
                            counter+=1
                        i+=1
                    saved[counter][0] = 1
                    data=printme(saved,scr)
                elif data[where] == "{" and data[where+1]==".":
                    i, counter = 0, -1
                    while i <= where:
                        if (data[i] == "[" and data[i + 1] != "]") or (data[i] == "{" and data[i + 1] != "}"):
                            counter += 1
                        i += 1
                    saved[counter][0] = 1
                    data = printme(saved, scr)
                else:
                    t,k=1,0
                    if data[where+1]=="]":
                        k+=1
                    while t != 0:
                        k += 1
                        if data[where + k] == "]":
                            t -= 1
                        elif data[where + k] == "[":
                            t += 1
                        elif data[where + k] == "/":
                            curser_y += 1
                            line += 1
                    curser_x, o = gonear(line, data)
            scr.move(curser_y,curser_x)
        except:
            continue
    curses.endwin()
with open("mahyar.json") as f:
    data=f.read()
data=data[:len(data)-1]
if __name__=="__main__":
    main(data)