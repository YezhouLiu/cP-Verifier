MACHINE simplecp
VARIABLES state,d,b,a,c
INVARIANT state >= 0 & d >= 0 & b >= 0 & a >= 0 & c >= 0
INITIALISATION state := 1; d := 0; b := 0; a := 10; c := 0
OPERATIONS
r1 = PRE state = 1 & a >= 2 THEN a := a - 2; b := b + 1; state := 1 END;
r2 = PRE state = 1 & b >= 2 THEN b := b - 2; c := c + 1; d := d + 2; state := 1 END
END
CompletedProcess(args=['probcli', 'simplecp.mch'], returncode=0, stdout=b'\r\n')
