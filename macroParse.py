def pass1(macro):
    l = len(macro)
    if l == 0 : return
    ci = l-1
    result = []
    while ci >= 0:
        a = macro[ci]
        if a == "'":
            ci -= 1
            result.insert(0,macro[ci] + a)
            ci -= 1            
        else:
            ci -= 1            
            result.insert(0,a)
    return result

def pass2(macro):
    si = 0
    l = len(macro)
    result = []
    tmp = []
    ci = 0
    while ci < l:
        a = macro[ci]
        if a == "(" :
            ci += 1
            si = ci
        elif a == ")":
            tmp = macro[si:ci]
            ci += 1
        elif a == "2":
            result.extend(tmp)
            ci += 1
        else:
            result.append(a)
            tmp = [a]
            ci += 1
    return result
	
def pass3(macro):
    tmp1 = [[ord(y) for y in x] for x in macro]
    tmp2 = [sum(x) for x in tmp1]
    tmp3 = tmp2[1:] + [0]
    tmp4 = list(zip(tmp2,tmp3))
    tmp5 = [x[0] - x[1] for x in tmp4]
    
    si = 0
    l = len(macro)
    result = []
    while si < l:
        if tmp5[si] == 39 or tmp5[si] == -39:
            si +=1
        else:
            result.append(macro[si])
        si += 1
    return result
    
def parseAdvice(macro):
    if macro == "":
        return ""
    macro1 = pass1(macro)
    macro2 = pass2(macro1)
    macro3 = pass2(macro2)
    macro4 = pass3(macro3)
    return macro4

#print(parseAdvice("xUU'yU'U(rUF)(RU2RU)2(FUr)"))
