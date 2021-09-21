Commas (,) are temporary allowed in the term or rule parsers.

About ParseTerm():
spaces are allowed, for example:
'p(u(Xm(Y)) n(Z)s(SY ))' can be correctly parsed to a Term object by calling 
t1 = ParseTerm('p(u(Xm(Y)) n(Z)s(SY ))')

About ParseTerms():
string terms are splitted with spaces ' '
for example, ParseTerms('f(a) b c g(Xt(y)h) c') will return a dictionary, which is: 
{f(a):1, b:1, c:2, g(Xt(y)h):1}

About ParseRule():
As an early implementation, I used blank space ' ' to separate each object in a rule,
such as l_state, r_state, ->+, | and each first-level term

Thus, a rule which can be parsed should looks like:
's1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))'
rather than 's1 ->+ s1 p( u(Xm(Y)) n(Z) s(SY) ) | p( u(X) n(Zm(Y)) s(S) )', which cannot be properly parsed.

Simpler examples:
which works properly:
's1 p(f(a)g(b)) h(X) d ->+ s1' 

which do not work properly at this moment:
's1 p(f(a)g(b))h(X) d ->+ s1' 
's1 p(f(a) g(b)) h(X) d ->+ s1' 
's1 p(f(a)g(b)) h(X)d ->+ s1'

All in all, each FIRST-LEVEL TERM in a rule should be separate by a blank space ' ',
and earh term itself should be written tightly, without using any space in it.

About calling the ProB model checker, see Bexample.py:
ProBMCCustom(ruleset, system_terms, system_state, system_name, '-bf -mc 1000')
As an experimental functionality, only rules with atoms are supported, all the rules will run in exact-once model.
To use the ProB model checking functionality, users need to install the latest version of ProB, and properly configure probcli.