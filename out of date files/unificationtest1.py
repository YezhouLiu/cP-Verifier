from compoundterm import CPTerm
from compoundrule import CPRule
from compoundcpsystem import CPSystem
from cpparser import ParseTerm
from cpparser import ParseRule
import sys

rule1 = ParseRule('s0 a(XYc(Z)) b(Xd(ZW)) ->+ s1 x(X) y(Y) z(Z) w(W)')
sys1 = CPSystem('s0')
sys1.AddRule(rule1)
sys1.AddTerm(ParseTerm('a(g() h() c(h()) )'))
sys1.AddTerm(ParseTerm('b( f() d(j() k()) )'))
sys1.AddTerm(ParseTerm('a( g() j() c(j()) )'))
sys1.AddTerm(ParseTerm('b( g() d(j() k()) )'))
sys1.Run()

rule2 = ParseRule('s0 a(XYc(ZW)) b(Xd(Z)) ->+ s1 x(X) y(Y) z(Z) w(W)')
sys2 = CPSystem('s0')
sys2.AddRule(rule2)
sys2.AddTerm(ParseTerm('a(g() h() c(h()k()) )'))
sys2.AddTerm(ParseTerm('b( f() d(h()) )'))
sys2.AddTerm(ParseTerm('a( g() j() c(j()k()) )'))
sys2.AddTerm(ParseTerm('b( g() d(j()) )'))
sys2.Run()