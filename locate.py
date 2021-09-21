

def locate(s='', to_insert='', x=0, y=0, insertx=False, inserty=False, *, ignore=[], shiftx=0, shifty=0):
    strArr = str(s).split('\n')
    insArr = str(to_insert).split('\n')

    if y < 0:
        y = len(strArr) + y
    y += shifty

    if inserty:
        for i in range(len(insArr)):
            strArr.insert(y, '')
    else:
        while len(strArr) < y+len(insArr):
            strArr.append('')

    if x < 0:
        if inserty:
            print('Cannot have negative x value with inserty to True')
            exit(0)
        
        x = len(strArr[y])+x
    x += shiftx

    maxLenStr = max([len(c) for c in strArr]) 
    maxLenIns = max([len(c) for c in insArr]) 
    for i in range(len(strArr)):
        while len(strArr[i]) < x+maxLenIns:
            strArr[i] += ' '

    for i, c in enumerate(insArr):
        if insertx:
            s1 = strArr[y+i][:x]
            s2 = strArr[y+i][x:]
            strArr[y+i] = s1+c+s2
        else:
            s1 = strArr[y+i][:x]
            s2 = strArr[y+i][x+len(c):]
            rep = list(strArr[y+i][x:x+len(c)])
            lc = list(c)

            for j in range(len(lc)):
                if lc[j] in ignore:
                    lc[j] = rep[j]
            strArr[y+i] = s1+''.join(lc)+s2

    return '\n'.join([s.rstrip() for s in strArr])





if __name__ == '__main__':

    s = ''

    s += 'Hello,\n'
    s += 'My name is \n'
    s += 'I am  years old\n'
    s += 'Goodbye'

    s = locate(s, 'John', 11, 1)
    s = locate(s, '19', -1, 2, True)

    ins = ''
    ins += 'I live in Washington\n'
    ins += 'I love potatoes'

    s = locate(s, ins, 0, 3, True, True)

    print(s)