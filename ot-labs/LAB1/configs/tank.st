PROGRAM prog0
  VAR
    level AT %IW100 : INT;
    pump AT %QX100.0 : BOOL;
  END_VAR

  IF level < 300 THEN
    pump := TRUE;
  ELSIF level > 700 THEN
    pump := FALSE;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#100ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : prog0;
  END_RESOURCE
END_CONFIGURATION
