import re
from typing import Union
from Stack import stack

def boolean(equation):
    operators = [TList["lst"], TList["gte"], TList["grt"], TList["lte"], TList["equ"], TList["nequ"]]
    for i in range(0, len(operators)):
        hasToken = f' {operators[i]} ' in equation
        if not hasToken:
            continue

        expression1, expression2 =        equation.split(operators[i])
        value1 = expression(expression1)
        value2 = expression(expression2)
        tk = operators[i]
        if tk == operators[0]:
            return value1 < value2
        if tk == operators[1]:
            return value1 > value2
        if tk == operators[2]:
            return value1 >= value2
        if tk == operators[3]:
            return value1 <= value2
        if tk == operators[4]:
            return value1 == value2
        if tk == operators[5]:
            return value1 != value2

    raise Exception("Invalid boolean expression")
datatypes = {"XS", "S", "L", "XL"}

class BinaryNode:
    val: Union[str,int]
    def __init__(self, val = "") -> None:
        self.right = None
        self.left = None
        self.val = val
      
def indexPairBracket(st, startBracket, endBracket, startIndex):
    bracketCounter = 1
    currentIndex = startIndex + 1
    while bracketCounter > 0:
        if currentIndex >= len(st):
            raise Exception("Invalid Expression")
        if st[currentIndex] == startBracket:
            bracketCounter = bracketCounter + 1
        elif st[currentIndex] == endBracket:
            bracketCounter = bracketCounter - 1  
        currentIndex = currentIndex + 1
    return currentIndex

def inParenthesis(exp):
    if exp[0] != TList["open"]:
        return False
    val = indexPairBracket(exp, TList["open"], TList["CLOSE"], 0)
    return val >= len(exp)

def tree(exp, node: BinaryNode):
    exp = exp.strip()
    if inParenthesis(exp):
        exp = exp[1:len(exp)-1]
    if not exp:
        raise Exception("Invalid Expression")
    if len(exp) == 0:
        return 
    if exp.isnumeric():
        node.val = int(exp)
        return

    temp = exp
    index_plus = None;
    index_minus = None;
    index_mul = None;
    index_div = None;
    index_mod = None;
    i = 0 
    while i < len(temp):
        if temp[i] == TList["open"]:
            i = indexPairBracket(temp, TList["open"], TList["close"],i)
        elif temp[i-1:i+2] == f' {TList["add"]} ':
            index_plus = i
        elif temp[i-1:i+2] == f' {TList["sub"]} ':
            index_minus = i
        elif temp[i-1:i+2] == f' {TList["mul"]} ':
            index_mul = i
        elif temp[i-1:i+2] == f' {TList["div"]} ':
            index_div = i
        elif temp[i-1:i+2] == f' {TList["mod"]} ':
            index_mod = i
        i = i + 1

    if index_plus or index_minus or index_mul or index_div:
        node.left = BinaryNode("")
        node.right = BinaryNode("")
    else:
        if  exp not in stack or stack[exp][1] == None:
            raise Exception("Vairable does not exist")
        if stack[exp] != None:
            node.val = stack[exp][1]
        return 
    if index_mul:
        node.val = TList["mul"]
        tree(exp[0:index_mul], node.left)
        tree(exp[index_mul+2:], node.right)
        return 
    if index_plus:
        node.val = TList["add"]
        tree(exp[0:index_plus], node.left)
        tree(exp[index_plus+2:], node.right)
        return 
    if index_minus:
        node.val = TList["sub"]
        tree(exp[0:index_minus], node.left)
        tree(exp[index_minus+2:], node.right)
        return 
    if index_div:
        node.val = TList["div"]
        tree(exp[0:index_div], node.left)
        tree(exp[index_div+2:], node.right)
        return 
    if index_mod:
        node.val = TList["mod"]
        tree(exp[0:index_mod], node.left)
        tree(exp[index_mod+2:], node.right)
        return 
      
def solveTree(node: BinaryNode):
    if not node:
        return 0
    if type(node.val) is int:
        return node.val
    if node.val == TList["add"]:
        return solveTree(node.left) + solveTree(node.right)
    elif node.val == TList["sub"]:
        return solveTree(node.left) - solveTree(node.right)
    elif node.val == TList["mul"]:
        return solveTree(node.left) * solveTree(node.right)
    elif node.val == TList["div"]:
        denom = solveTree(node.right)
        if denom == 0:
            raise Exception("Division by Zero")
        return int(solveTree(node.left) / denom)
    elif node.val == TList["mod"]:
        if denom == 0:
            raise Exception("Division by Zero")
        return int(solveTree(node.left) % denom)

def expression(exp:str):
    exp = exp.strip()
    root = BinaryNode()
    tree(exp, root)
    return solveTree(root)

def insideBrackets(statement, startBracket, endBracket):
    bracketCounter = 1
    currentIndex = 1
    while bracketCounter > 0 :
        if statement[currentIndex] == startBracket:
            bracketCounter += 1
        elif statement[currentIndex] == endBracket:
            bracketCounter -= 1
        currentIndex += 1
    return [statement[1:currentIndex-1], statement[currentIndex:]]

TList = {
    'assign': "=",
    'end': "End",
    'start': "Start",
    'cond': "cond",
    'rerun': "rerun",
    'add': "+",
    'sub': "-",
    'mul': "*",
    'div': "/",
    'mod': "%",
    'gte': ">",
    'lst': "<",
    'gte': ">=",
    'lte': "<=",
    'equ': "==",
    'nequ': "!=",
    'open': "(",
    'close': ")",
    'blstart': "{",
    'blend': "}",
}