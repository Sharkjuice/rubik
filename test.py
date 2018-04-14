import pdb
def parseAdvice(macro):
    l = len(macro)
    if l == 0 : return
    ci = l-1
    pass1 = []
    while ci >= 0:
        a = macro[ci]
        if a == "'":
            ci -= 1
            pass1.insert(0,macro[ci] + a)
            ci -= 1            
        else:
            ci -= 1            
            pass1.insert(0,a)
            
    si = 0
    l = len(pass1)
    pass2 = []
    tmp = []
    ci = 0
    while ci < l:
        a = pass1[ci]
        if a == "(" :
            ci += 1
            si = ci
        elif a == ")":
            #pass2.extend(pass1[si:ci])
            tmp = pass1[si:ci]
            ci += 1
        elif a == "2":
            pass2.extend(tmp)
            ci += 1
        else:
            pass2.append(a)
            tmp = [a]
            ci += 1
            
    print("pass2: ", pass2)        

  
    return pass2

print(parseAdvice("(rUF)(RU2RU)2(FUr)"))
