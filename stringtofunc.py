import math

'''
#testing code:
class dummy:
    val = 0.0
    def __init__(self, v):
        self.val = v
print tofunction("( + ( sin a ) pi )")({"a":dummy(1)})
'''

def tofunction(s):
    tokens = s.split()
    return listtofunc(tokens, [])

def isnumber(s):
    try:
        a = float(s)
        return True
    except ValueError:
        return False

def isvar(s):
    c = ord(s[0])
    return (c >= 65 and c < 91) or (c >= 97 and c < 123)

def listtofunc(tokens, stack):
    if len(tokens) == 0:
        return stack[0]
    token = tokens.pop()
    if token == ")":
        stack.append(listtofunc(tokens, []))
    elif token == "(":
        return stack[0]
    elif isnumber(token):
        n = float(token)
        stack.append((lambda vrs : n))
    elif token == "sin":
        f = stack.pop()
        stack.append((lambda vrs : math.sin(f(vrs))))
    elif token == "cos":
        f = stack.pop()
        stack.append((lambda vrs : math.sin(f(vrs))))
    elif token == "pi":
        stack.append((lambda vrs : 3.14159265358979))
    elif token == "+":
        f = stack.pop()
        g = stack.pop()
        stack.append((lambda vrs : f(vrs) + g(vrs)))
    elif token == "*":
        f = stack.pop()
        g = stack.pop()
        stack.append((lambda vrs : f(vrs) * g(vrs)))
    elif token == "/":
        f = stack.pop()
        g = stack.pop()
        stack.append((lambda vrs : f(vrs) / g(vrs)))
    elif token == "-":
        f = stack.pop()
        g = stack.pop()
        stack.append((lambda vrs : f(vrs) - g(vrs)))
    elif isvar(token):
        stack.append((lambda vrs : vrs[token].val))
    return listtofunc(tokens, stack)
