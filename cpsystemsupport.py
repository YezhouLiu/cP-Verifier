from term import Term

def ValidSystemTerm(t1):
  if isinstance(t1, Term) and t1.IsGround():
    return True
  elif t1 == '1':
    return True
  elif t1 >= 'a' and t1 <= 'z':
    return True
  else:
    return False 