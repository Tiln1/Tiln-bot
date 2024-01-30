from __future__ import division
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator
import numpy
import random
from decimal import Decimal, getcontext, ROUND_HALF_UP
import asyncio
import concurrent.futures as futures
from functools import partial
from scipy.special import gamma, lambertw

from otherStuff import HelpMethods  # @UnresolvedImport
hm = HelpMethods()

pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986'
e = '2.71828182845905'
phi = '1.618033988749895'

class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        pi = CaselessLiteral("PI")
        phi = CaselessLiteral("PHI")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + pi + phi + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        mod = Literal("%")
        fact = Literal("!")
        sl = Literal("<<")
        sr = Literal(">>")
        ande = Literal("&")
        orr = Literal("|")
        xor = Literal("$")
        nott = Literal("~")
        down = Literal("↓↓")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        rt = Literal("~~")
        addop = plus | minus
        multop = mult | div | mod | sl | sr | ande | orr | xor | rt | nott | fact | down
        expop = Literal(":") | Literal("^")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | phi | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        # epsilon = 1e-12
        self.opn = {
                    # "/%": self.decdivrem,
                    "+": operator.add,
                    "-": operator.sub,
                    "/": self.decdiv,
                    "*": self.decmult,
                    "%": self.decmod,
                    ">>": self.shiftright,
                    "<<": self.shiftleft,
                    "&": self.anding,
                    "|": self.orring,
                    "$": self.xorring,
                    "~~": self.roundto,
                    "~": self.notting,
                    "^": self.decpow,
                    "!": self.fact,
                    "↓↓": self.down,
                    ':': self.sum2
                    }
        self.fn = {"sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "asin": math.asin,
                    "acos": math.acos,
                    "atan": math.atan,
                    "exp": math.exp,
                    "abs": abs,
                    "trunc": lambda a: int(a),
                    "round": round,
                    "log": math.log,
                    "log10": math.log10,
                    "sqrt": self.sqrt,
                    "sgn": self.sign,
                    "fact": self.fact,
                    "ceil": self.ceil,
                    "floor": self.floor,
                    "randint": self.randint,
                    "rand": self.rand,
                    "rev": self.rev,
                    "rtd": self.rtd,
                    "dtr": self.dtr,
                    "sum": self.sum,
                    "lambertw": self.lambertw,
                    "lwopt": self.lwopt
#                    "print": self.printer
                   }
#                  "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        sigdig = 1550
        if getcontext().prec != sigdig:
            getcontext().prec = sigdig
            getcontext().rounding = ROUND_HALF_UP
        op = s.pop()
        if op == 'unary -':
            return self.evaluateStack(s) * -1
        if op in self.opn.keys():
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return Decimal(pi)
        elif op == "E":
            return Decimal(e)
        elif op == "PHI":
            return Decimal(phi)
        elif op in self.fn.keys():
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            if len(op.split('.', 1)[0])>40 or int(Decimal(op)) == Decimal(op) or '.000000000000000' in op or '.999999999999999' in op:
                if '.999999999999999' in op:
                    return int(op.split('.', 1)[0]) + 1
                return int(Decimal(op))
            else:
                getcontext().rounding = ROUND_HALF_UP
                getcontext().prec = 42
                op = str(Decimal(op)+0)
                while op[-1] == '0' and len(str(op)) > 1:
                    op = op[:-1]
                return Decimal(op)
           
    async def eval(self, num_string, parseAll=True):
#         async def eval2(num_string, parseAll=True):
        self.exprStack = []
#         try:
        self.bnf.parseString(num_string, parseAll)
#         except: return 0
        
        loop = asyncio.get_event_loop()
        pool = futures.ThreadPoolExecutor()
        func = partial(self.evaluateStack, self.exprStack)
        future = loop.run_in_executor(pool, func)
        
        val = await asyncio.wait_for(future, 3)
        
        if val == 0:
            return
        
        val = str(val)
        if len(val.split('.', 1)[0])>27 or int(Decimal(val)) == Decimal(val) or '.0000000000000' in val or '.999999999999999' in val:
            if '.999999999999999' in val:
                return int(val.split('.', 1)[0]) + 1
            return int(Decimal(val))
        else:
            getcontext().rounding = ROUND_HALF_UP
            getcontext().prec = 42
            val = str(Decimal(val)+0)
            while val[-1] == '0' and len(str(val)) > 1:
                val = val[:-1]
            return Decimal(val)
#         post_thread = Thread(target=await eval2, args=(num_string, parseAll))
#         post_thread.start()
    
    def fact(self, num, useless=0):
        if num > 300 or num <= -1:
            return 'error'
        if str(num).isdigit():
            return Decimal(math.factorial(int(num)))
        else:
            return Decimal(gamma(float(num)+1))
        
    
    # def decdivrem(self, a, b):
    #     return Decimal(a)/Decimal(b)

    def decdiv(self, a, b):
        return Decimal(a)/Decimal(b)
    
    def decdiv2(self, a, b):
        return int(Decimal(a)/b)
    
    def decpow(self, a, b):
        b = Decimal(b)
        if Decimal(math.log10(a))*b > 310:
            return 'error'
        return Decimal(a)**b
    
    def decmult(self, a, b):
        return Decimal(a)*Decimal(b)
    
    def decmod(self, n, m):
        n = Decimal(n)
        m = Decimal(m)
        return Decimal(n - self.floor(n / m) * m)
            
    def rand(self, maximum):
        return Decimal(random.SystemRandom().uniform(0, maximum))
    
    def randint(self, maximum):
        return Decimal(random.SystemRandom().randint(1, maximum))
    
    def sqrt(self, num):
        return Decimal(abs(num))**Decimal(0.5)
    
    def sign(self, num):
        return numpy.sign(int(num))
    
    def rev(self, num):
        return int(str(num)[::-1])
    
    def rtd(self, num):
        return Decimal(num)*Decimal(360*(1/(2*math.pi)))
    
    def dtr(self, num):
        return Decimal(num)*Decimal((1/360)*2*math.pi)
    
#     def printer(self, var):
#         hm.getprevvar(self.uid, var)

    def lambertw(self, num):
        return Decimal(lambertw(float(num)).real)
    def lwopt(self, num):
        return Decimal(e)**(Decimal(lambertw(float(Decimal(num) * Decimal(e))).real) - 1)

    def ceil(self, num):
        if num > 0:
            return int(num + Decimal(0.999999999999999999999999999999999999999))
        elif num < 0:
            return int(num)
        return 0
    
    def floor(self, num):
        if num > 0:
            return int(num)
        elif num < 0:
            return int(num - Decimal(0.999999999999999999999999999999999999999))
        return 0
    
    def down(self, a, b):
        def down2(a1, a, b):
            if b == 2:
                return self.decpow(a1, a)
            return down2(self.decpow(a1, a), a, b-1)
        return down2(a, a, b)
    
    def sum2(self, a, b):
        a = int(a)
        b = int(b)
        if(max(len(str(a)), len(str(b))) > 10000):
            return 'error'
        return ((abs(b-a)+1)*(a+b))//2
    
    def sum(self, num):
        tot = 0
        for x in str(int(num)):
            tot += int(x)
        return tot
    
    def roundto(self, a, b):
        return round(Decimal(a), b)
    
    def shiftright(self, a, b):
        return a//2**b
        
    def shiftleft(self, a, b):
        return a*2**b
    
    def xorring(self, a, b):
        return a^b
    def orring(self, a, b):
        return a|b
    def anding(self, a, b):
        return a&b
    def notting(self, useless, a):
        a = abs(a)
        l = len(bin(a))-2
        count = 0
        while(True):
            if 2**count >= l:
                l = 2**count
                break
            count += 1
        return int('0b'+'1'*l, 2) - a
    
