from turtle import *
import json
from math import sin,cos,pi


def mymain():
    f = open("client.json")
    s=f.read()
    f.close()
    s = json.loads(s)
    w = s["width"]
    h = s["height"]
    setup(width=w, height=h, startx=None, starty=None)
    t = Turtle()
    screen = Screen()
    screen.screensize(h, w)
    screen.colormode(255)
    s = s["functions"]
    t.hideturtle()

    funcdict = {}
    for func in s:
        funcdict[func["function name"]] = func

    def argsmaker(arg):
        try:
            arg = int(arg)
        except:
            pass
        if type(arg) == type(1):
            return arg
        elif arg['type'] == 'function call':
            return runfunc(arg['function name'], arg['args'])
        else:
            if arg['type'] == '+':
                return argsmaker(arg['A']) + argsmaker(arg['B'])
            elif arg['type'] == '-':
                return argsmaker(arg['A']) - argsmaker(arg['B'])
            elif arg['type'] == '*':
                return argsmaker(arg['A']) * argsmaker(arg['B'])
            elif arg['type'] == '/':
                return argsmaker(arg['A']) / argsmaker(arg['B'])
            elif arg['type'] == '%':
                return argsmaker(arg['A']) % argsmaker(arg['B'])

    def runrecfunc(fulldict, args):
        base = str(fulldict['base expression'])
        rec = str(fulldict['recursive expression'])
        i = 0
        while i < len(args) - 1:
            base = base.replace("'" + fulldict['args'][i] + "'", str(argsmaker(args[i])))
            i += 1
        base = base.replace("'", '"')
        base = json.loads(base)
        r = argsmaker(base)
        i = 0
        while i < len(args) - 1:
            rec = rec.replace("'" + fulldict['args'][i] + "'", str(argsmaker(args[i])))
            i += 1
        for i in range(1, argsmaker(args[-1]) + 1):
            rec2 = rec.replace("'r'", str(r))
            rec2 = rec2.replace("'n'", str(i))
            rec2 = rec2.replace("'", '"')
            rec2 = json.loads(rec2)
            r = argsmaker(rec2)
            rec2 = str(rec2)
        return r

    def runfunc(name, args):
        finarg = {}
        i = 0
        if name == "if":
            if argsmaker(args[0]) != 0:
                return argsmaker(args[1])
            else:
                return argsmaker(args[2])
        if name == "drawLine":
            t.penup()
            t.goto(argsmaker(args[0]) - w / 2 + 6, argsmaker(args[1]) - h / 2 - 6)
            t.pencolor(argsmaker(args[4]), argsmaker(args[5]), argsmaker(args[6]))
            t.pendown()
            t.goto(argsmaker(args[2]) - w / 2 + 6, argsmaker(args[3]) - h / 2 - 6)
            return 0
        elif name == "drawPoint":
            t.pencolor(argsmaker(args[2]), argsmaker(args[3]), argsmaker(args[4]))
            t.penup()
            t.goto(argsmaker(args[0]) + 6 - w / 2, argsmaker(args[1]) - 6 - h / 2)
            t.pendown()
            t.circle(1)
            return 0
        elif name == "drawCircle":
            t.penup()
            t.goto(argsmaker(args[0]) + 6 - w / 2, argsmaker(args[1]) - argsmaker(args[2]) - 6 - h / 2)
            t.pencolor(argsmaker(args[3]), argsmaker(args[4]), argsmaker(args[5]))
            t.pendown()
            t.circle(argsmaker(args[2]))
            return 0
        elif name == "drawEllipse":
            def ellipse(t, x, y, r1, r2, r, g, b):
                t.penup()
                t.pencolor(r, g, b)
                t.goto(x + r1 / 2 + 6 - w / 2, y + 2 * r2 / 2 - 6 - h / 2)
                t.pendown()
                penx, peny = t.pos()
                for i in range(360):
                    penx += cos(i * pi / 180) * r1 / 180
                    peny += sin(i * pi / 180) * r2 / 180
                    t.goto(penx, peny)
                t.penup()
                return 0

            return ellipse(t, argsmaker(args[0]), argsmaker(args[1]), argsmaker(args[2]), argsmaker(args[3]),
                           argsmaker(args[4]), argsmaker(args[5]), argsmaker(args[6]))
        if funcdict[name]['type'] == "recursive function definition":
            return runrecfunc(funcdict[name], args)

        s = str(funcdict[name]['expression'])
        while i < len(args):
            s = s.replace("'" + funcdict[name]['args'][i] + "'", str(argsmaker(args[i])))
            i += 1
        result = ''
        s = s.replace("'", '"')
        s = json.loads(s)
        return argsmaker(s)

    runfunc('main', [])

    t.getscreen().getcanvas().postscript(width=w,height=h,file="image1.ps")


#mymain()