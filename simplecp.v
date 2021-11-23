(*simplecp*)
From CP Require Export operations.
From Coq Require Import Lists.List.
Import ListNotations.

Definition cPsys1 := cP_sys (s 1) [Atom a; Atom a; Atom a; Atom a; Atom a; Atom a; Atom a; Atom a; Atom a; Atom a].

Definition r1 (sys:cPsystem_conf) : cPsystem_conf :=
match sys with
| cP_sys (s 1) terms =>
if AtomBagIn [Atom a; Atom a] terms then ChangeState (s 1) (ProduceATerm (Atom b) (ConsumeATerm (Atom a) (ConsumeATerm (Atom a) sys)))
else sys
| _ => sys
end.
Definition r0 (sys:cPsystem_conf) : cPsystem_conf :=
match sys with
| cP_sys (s 1) terms =>
if AtomBagIn [Atom b; Atom b] terms then ChangeState (s 1) (ProduceATerm (Atom d) (ProduceATerm (Atom d) (ProduceATerm (Atom c) (ConsumeATerm (Atom b) (ConsumeATerm (Atom b) sys)))))
else sys
| _ => sys
end.

