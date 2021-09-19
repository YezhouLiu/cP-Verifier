About the term parser:
spaces are allowed, for example:
'p(u(Xm(Y)) n(Z)s(SY ))' can be correctly parsed to a Term object by calling 
t1 = ParseTerm('p(u(Xm(Y)) n(Z)s(SY ))')

About the rule parser:
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
