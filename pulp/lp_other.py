# coding:utf-8
import time
import math
import sympy

def solve(r):
    _r = math.ceil(r)
    _rp = reversed(sorted(set(rp)))
    for i in _rp:
        tmp = _r//i
        _r = _r - i*tmp
        print(tmp,i,_r)


rp = [329,149,99,99,229,149,99]
sorted(set(rp))

r1 = 500000 * (599.26/100 -2/100)
x1 = r1 + 1867800

x2 = 1877000 * (1/100 + 0.49/100) + 1877000
r2 = x1 - x2

if r2 < 0:
    # 满足
    print(r1)
    print("ok")
    solve(r1)
else:
    x3 = 3215212 - (r2)
    x4 = 3212000*(0.1/100)+3212000
    r3 = x3 - x4
    if r3 <0:
        print(r2)
        print("ok")
        solve(r2)
    else:
        x5 = ((1-0.93)/100 + 1/100)*1335000
        r4 = r3 -x5
        if r4 <0:
            print(r3)
            print("ok")
        else:
            xx2 = 845000 * (1.98/100 +2/100)
            xx3 = 532000 * (1.95/100 +2/100)

            if r4 - xx2 < 0:
                print(r4)
                print("ok")
            else:
                if r4 - xx2 -xx3 < 0:
                    print(r4 - xx2)
                    print("ok")
                else:
                    print(r4 - xx2 -xx3)





