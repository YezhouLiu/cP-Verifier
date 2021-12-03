# How to Use

- Commas (,) are temporary allowed in the term or rule parsers.
- Each FIRST-LEVEL TERM in a rule should be separate by a blank space `' '`
- Each term itself should be written tightly, without using any space in it

# ParseTerm()

- Spaces are allowed. Example:

  - `p(u(Xm(Y)) n(Z)s(SY ))` can be correctly parsed to a Term object by calling
    `t1 = ParseTerm('p(u(Xm(Y)) n(Z)s(SY ))')`

- String terms are splitted with spaces `' '`. Example:
  - ParseTerms`('f(a) b c g(Xt(y)h) c')` will return a dictionary, which is:
    `{f(a):1, b:1, c:2, g(Xt(y)h):1}`

# ParseRule()

As an early implementation, I used blank space ' ' to separate each object in a rule,
such as `l_state, r_state, ->+, | and each first-level term`

- Example can be parsed:
  ```
  s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))
  ```
- Example can NOT be parsed:

  ```
  s1 ->+ s1 p( u(Xm(Y)) n(Z) s(SY) ) | p( u(X) n(Zm(Y)) s(S) )
  ```

- Simpler examples which works properly:

  ```
  s1 p(f(a)g(b)) h(X) d ->+ s1
  ```

- Example NOT work properly at this moment:

  ```
  s1 p(f(a)g(b))h(X) d ->+ s1
  s1 p(f(a) g(b)) h(X) d ->+ s1
  s1 p(f(a)g(b)) h(X)d ->+ s1
  ```

# ProB model checker

Refer to `Bexample.py`

```
ProBMCCustom(ruleset, system_terms, system_state, system_name, '-bf -mc 1000')
```

As an experimental functionality, **only rules with atoms are supported**
cP systems do not have virtual product membranes, all the rules will run in `exact-once model`.

To use the ProB model checking functionality, user needs to install the latest version of [ProB](https://www.probesoftware.com/), and properly configure probcli.

Similarly, to use PAT3 automated verification, user needs to install `PAT3` software and configure corresponding environment variables.
