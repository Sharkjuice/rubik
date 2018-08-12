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
    tmp2 = [[(lambda z:(z == 39) * 100 + z)(y) for y in x] for x in tmp1]
    tmp3 = [sum(x) for x in tmp2]
    tmp4 = tmp3[1:] + [0]
    tmp5 = list(zip(tmp3,tmp4))
    tmp6 = [x[0] - x[1] for x in tmp5]
    
    si = 0
    l = len(macro)
    result = []
    while si < l:
        if tmp6[si] == 139 or tmp6[si] == -139:
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
#print(parseAdvice("y(RU'R)(URUR)(U'R'U'R')R"))
