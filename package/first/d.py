import sys
sys.path.append("..")
from second.c import calc_minus

def calc_add_minus(a, b):
    ans = a + b
    ans = calc_minus(a=ans, b=0)

    return ans
