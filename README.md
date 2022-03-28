# How to use:

1. A compiled desktop version (`.exe`) of cPV is under the `Released` folder.
   The `main.exe` is the entry to the programme.
2. For the console version, example python files can be found under the `examples` folder.

# How to represent cP systems

## Load from File

We proposed a JSON format for cP systems, namely cPVJ. Example files can be found under the `examples` folder.

In the desktop version of cPV, examples of cPVJ files can be loaded via menu bar.

Users can also open the `.JSON` files and check their details.

## Input from UI

cP systems can also be inputed via the UI interface provided by the desktop version of `cPV`, and be saved as `cPVJ` files.

A cP system should contain the following 4 parts:

1. A system name, which is an arbitrary string.
2. The initial state of the system. For example, s0, s1, or s2.
3. Initial system terms, which is a number of key-value pairs separated by semicolons `(;)`.

   - For example, if the system contains 3 copies of f(a), 2 copies of b, 1 copy of c.
     Users can input the following terms in `Initial terms` :

     ```
     f(a):1; b:2; c:1;
     ```

   - Notice that whitespaces and `\n` will be ignored in the `Initial terms` field.

4. Rules, which are one or more rules separated by semicolons `(;)`.

   - Example:

     ```
     s0 ->1 s1 p(n(M)s()u()) | m(M) ;
     s1 ->1 s2 o(X) | p(As(T)u(X)) t(T) ;
     s1 ->1 s3 o() | p(An()) ;
     s1 ->+ s1 p(n(Z)s(SY)u(Xm(Y))) | p(n(Zm(Y))s(S)u(X)) ;
     s1 p(A) ->+ s1 ;
     ```

   - Notice that each term, state, arrow`(->1 or ->+)` and bar`(|)` in a rule must be separated by whitespaces.
   - Please DO NOT add whitespaces inside a term, for example, please do not write f(abc) as f(a b c) in the `Rules` field.

   - Correct rule example:

     ```
     s1 ->+ s1 p(u(Xm(Y))n(Z)s(SY)) | p(u(X)n(Zm(Y))s(S))
     ```

   - Incorrect rule example:

     ```
     s1 ->+ s1 p( u(Xm(Y)) n(Z) s(SY) ) | p( u(X) n(Zm(Y)) s(S) )
     ```

# cPV verification:

Please try different buttons and see, most of them are straightforward.

For a cP system, if users what to do deadlock check, users need to specify which states are expected halting states.

This design is used to get rid of sinks -- otherwise they will be treated as deadlocks, since these states has no outgoing edge.

Additional specifications are used to perform verification related to terms and states -- to input them.

The format of them is the same to previous fields on terms and states.

# ProB model checker

Only command line version allows users to use their party tools to verify cP systems.

Refer to `Bexample.py` in `examples` folder

```
ProBMCCustom(ruleset, system_terms, system_state, system_name, '-bf -mc 1000')
```

As an experimental functionality, **only rules with atoms are supported.**

cP systems do not have virtual product membranes, all the rules will run in `exact-once model`.

To use the ProB model checking functionality, user needs to install the latest version of [ProB](https://www.probesoftware.com/), and properly configure probcli.

# PAT3 model checker

Similarly, to use PAT3 automated verification, user needs to install [PAT3](https://pat.comp.nus.edu.sg/) software and configure corresponding environment variables.

A file named `CSPexample.py` can be found in `examples` folder.
