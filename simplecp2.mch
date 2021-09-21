MACHINE simplecp2
VARIABLES state,a,b
INVARIANT state >= 0 & a >= 0 & b >= 0
INITIALISATION state := 1; a := 100; b := 90
OPERATIONS
r1 = PRE state = 1 & a >= 3 & b >= 1 THEN a := a - 3; b := b - 1; b := b + 1; state := 1 END;
r2 = PRE state = 1 & b >= 1 THEN b := b - 1; a := a + 1; state := 1 END
END
