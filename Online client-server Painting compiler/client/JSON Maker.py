import json
import requests
import shutil
allfuncs=["if",3,"drawPoint",5,"drawLine",7,"drawCircle",6,"drawEllipse",7]

class Error:
    def scaleError(line):
        return "Error on line 1 \n  %s \nscale Error: expected 2 number in first line that split with one space" % (line)
    def tabErrorb(nline,line):
        return "Error on line %s \n %s \ntab Error: expected 4 white space before base expression" % (nline, line)
    def tabErrorr(nline,line):
        return "Error on line %s \n %s \ntab Error: expected 4 white space before recursive expression" % (nline, line)
    def funcdefError(nline,line):
        return "Error on line %s \n %s \n FunctionDefinition Error: plz check how you define function"%(nline,line)
    def typeError(a,b,c):
        return "Error on line %s \n  %s \n %s" %(a,b,c)
    def runtime(a,b):
        return "Error on line %s \n  %s \nunexpected Error"%(a,b)


def funccall(s):  #this function get a function name with argomans and return json
    name,c="",0
    for i in s: #tell me the function name!
        if i=="(": break
        name+=i
        c+=1

    if name in allfuncs: #check if this function already defined or return error
        q, args, arg = 0, [], ""
        for i in s[c + 1:-1]: #remove name and paranteses and remain argomans
            if i == "(":
                q += 1
            elif i == ")":
                q -= 1
            if i == "," and q == 0:
                args.append(arg)
                arg = ""
                continue
            arg += i
        args.append(arg) #know args is a list that contain argomans splited
        if "" in args and len(args)>1: return "argument Error: check your function arguments"
        if len(args)!=allfuncs[allfuncs.index(name)+1]:
            return "Arguments number Error: expected %s arguments but %s given"%(allfuncs[allfuncs.index(name)+1],len(args))

        result = '{"type": "function call","function name":"%s","args":[' % (name)
        for arg in args:
            if "Error" not in expmaker(arg):result += expmaker(arg) + ","
            else: return expmaker(arg)
        return result[:-1] + "]}"
    else:
        return "Function name Error: %s is not defined"%(name)

def expmaker(exp):  #this function get a expression and return json
    def expmaker2(exp):
        explist = []
        myexp = ""
        q = 0
        for i in range(len(exp)):  # let's first split sections
            if exp[i] == "(": q += 1
            if exp[i] == ")": q -= 1
            if (exp[i] == "*" or exp[i] == "/" or exp[i] == "%") and q == 0:
                explist.append(myexp)
                myexp = ""
                explist.append(exp[i])
            else:
                myexp += exp[i]
        explist.append(myexp)
        if "" in explist and len(explist) > 1: return "operator Error: plz check your expression. their's something wrong"

        if len(explist) == 1:  # this is when we don't have any +-*/% in expression. it's maybe a function or just a variable
            if "(" in explist[0]:  # it's function
                return funccall(explist[0])

            else:  # it's variable
                try:
                    return str(int(explist[0]))
                except:
                    return '"%s"' % (explist[0])


        elif len(explist) > 1:  # this is when we have operators
            exp2 = ""
            for t in explist[2:]:
                exp2 += t
            if "Error" in expmaker2(explist[0]): return expmaker2(explist[0])
            if "Error" in expmaker2(exp2): return expmaker2(exp2)
            return '{"type":"%s","A":%s,"B":%s}' % (explist[1], expmaker2(explist[0]), expmaker2(exp2))
    explist = []
    myexp = ""
    q=0
    for i in range(len(exp)): #let's first split sections
        if exp[i]=="(":q+=1
        if exp[i]==")":q-=1
        if (exp[i] == "+" or exp[i] == "-") and q==0:
            explist.append(myexp)
            myexp=""
            explist.append(exp[i])
        else:
            myexp += exp[i]
    explist.append(myexp)
    if "" in explist and len(explist)>1: return "operator Error: plz check your expression. their's something wrong"

    if len(explist)==1: #this is when we don't have any +-*/% in expression. it's maybe a function or just a variable
        if '*' in explist[0] or '%' in explist[0] or '/' in explist[0]:
            return expmaker2(exp)
        if "(" in explist[0]: #it's function
            return funccall(explist[0])

        else: #it's variable
            try: return str(int(explist[0]))
            except: return '"%s"'%(explist[0])


    elif len(explist)>1: #this is when we have operators
        exp2=""
        for t in explist[2:]:
            exp2+=t
        if "Error" in expmaker2(explist[0]): return expmaker(explist[0])
        if "Error" in expmaker(exp2): return expmaker(exp2)
        return '{"type":"%s","A":%s,"B":%s}'%(explist[1],expmaker2(explist[0]),expmaker(exp2))

def funcdef(s): #this is when we define a new function. it,s get a full line of program and return json
    i , funcname , funcargs= 4 , "" , ""  #to start in start of function name
    result = '{"type":"function definition",'

    #find function name
    while s[i] != "(":
        funcname += s[i]
        i += 1
    result += '"function name": "%s",'%(funcname)
    print(allfuncs)
    if funcname not in allfuncs:allfuncs.append(funcname)  # know that we define this function let's add it to our funclist
    else: return "function name Error: this name is already taken"

    #find function arguments
    i += 1
    while s[i] != ")": #this find arguments
        funcargs += s[i]
        i += 1
    argslist = list(funcargs.split(","))
    if "" in argslist and len(argslist)>1: return "argument Error: check your function arguments"
    if funcname=="main" and len(argslist)>0 and argslist[0]!="": return "main function Error: main can't get any arguments"
    allfuncs.append(len(argslist))
    result += '"args": ['
    for arg in argslist:
        if arg=="":result+=","
        else:result+=('"' + arg + '"' + ',')
    result=result[:-1] + '],'


    i+=1
    exp=s[i:]
    if exp=="":return "function expression Error: your function must have expression"
    result+='"expression":'
    if "Error" in expmaker(exp):return expmaker(exp)
    result+=expmaker(exp)+"}"
    return result

def rfuncdef(s, exp0, expr): #this is when we define a new recursive function. it,s get a full line of program and return json
    i = 5  # to start in start of function name
    if exp0[0]!="0" :return "0 Error: expected '0' in base expression"
    elif expr[0]!="r":return "r Error: expected 'r' in recursive expression"

    #find function name
    funcname = ""
    funcargs = ""
    result = '{"type":"recursive function definition",'
    while s[i] != "(":
        funcname += s[i]
        i += 1
    result += '"function name": "%s",' % (funcname)
    if funcname not in allfuncs:allfuncs.append(funcname)
    else: return "function name Error: this name is already taken"

    #find function arguments
    i += 1
    while s[i] != ")":
        funcargs += s[i]
        i += 1
    argslist = list(funcargs.split(","))
    if "" in argslist: return "argument Error: check your function arguments"
    allfuncs.append(len(argslist))
    result += '"args": ['
    if len(argslist)!=1:
        for arg in argslist[:-1]:
            result += ('"' + arg + '"' + ',')
        result = result[:-1] + '],'
    else:result += "],"


    #check if Error happend
    if "Error" in expmaker(argslist[-1]):
        return expmaker(argslist[-1])
    if "Error" in expmaker(exp0[1:]):
        return expmaker(exp0[1:])+"'00'"
    if "Error" in expmaker(expr[1:]):
        return expmaker(expr[1:])+"'rr'"
    if exp0=="" or exp0[1:]=="": return "function expression Error: your recursive function must have base expression'00'"
    if expr=="" or expr[1:]=="": return "function expression Error: your recursive function must have recursive expression'rr'"
    result+='"recursive arg":%s,"base expression":%s,"recursive expression":%s}'%(expmaker(argslist[-1]),expmaker(exp0[1:]),expmaker(expr[1:]))
    return result


def readfile():
    f = open("mahyar.sp")
    s = f.read()
    f.close()
    return s

def main():
    s=readfile()
    lines = list(s.split("\n"))

    try:height, width = lines[0].split()
    except: return Error.scaleError(lines[0])

    result='{"height": %s,"width": %s,"functions": ['%(height,width)

    for _ in range(lines.count('')): lines.remove('')

    line=1
    while line < len(lines):
        newline = lines[line].replace(" ", "")


        if newline[0:4] == "func":
            try:value=funcdef(newline)
            except: return Error.runtime(line+1,lines[line])
            if "Error" in value:return Error.typeError(line+1,lines[line],value)
            else:result += value + ","


        elif newline[0:5] == "rfunc":

            #tab check
            if lines[line + 1][:4]!="    ":return Error.tabErrorb(line+2,lines[line+1])
            if lines[line+2][:4]!="    ":return Error.tabErrorr(line+3,lines[line+2])

            #check if an unexpected Error apear
            try:value=rfuncdef(newline, lines[line + 1].replace(" ", ""), lines[line + 2].replace(" ", ""))
            except:return Error.runtime(line+1,lines[line])

            #check if an expected Error apear
            if "Error" in value:
                if "'0'" in value:return Error.typeError(line+2,lines[line+1][4:],value)
                elif "'r'" in value:return Error.typeError(line+3,lines[line+2][4:],value)
                elif "'00'" in value:return Error.typeError(line+2,lines[line+1][4:],value[:-4])
                elif "'rr'" in value:return Error.typeError(line + 3, lines[line + 2][4:], value[:-4])
                else: return Error.typeError(line+1,lines[line],value)

            else:result+=value + ","

            line += 2
        #if the begging of a line don't start with func or rfunc
        else:
            return Error.funcdefError(line+1,lines[line])
        line += 1
    result = result[:-1] + "]}"
    if "main" not in allfuncs:
        return "main Error: you must define a function that named 'main'"
    return result

def req():
    jsn=main()
    res=requests.post("http://127.0.0.1:8877/job",json=jsn)
    i=res.json()
    r=requests.get("http://127.0.0.1:8877/job/{}".format(i))
    while True:
        z=requests.get("http://127.0.0.1:8877/job/{}".format(i))
        print(z.json())
        if z.json()!=r.json():
            break
    x=z.json()
    url=x["download url"]
    l=requests.get("http://127.0.0.1:8877{}".format(url),stream=True)
    with open('image.ps', 'wb') as out_file:
        shutil.copyfileobj(l.raw, out_file)
if "Error" not in main():
    req()
else:
    print(main())