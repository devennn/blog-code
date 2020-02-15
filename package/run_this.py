# run_this.py
import first
from second import c

def main():
    ans = first.calc_divide(a=4, b=3)
    print('calc_divide %d' %ans)

    ans = first.calc_plus(a=4, b=3)
    print('calc_plus %d' %ans)

    ans = c.calc_minus(a=5, b=4)
    print('calc_minus %d' %ans)

    ans = first.calc_add_minus(a=5, b=1)
    print('calc_add_minus %d' %ans)

if __name__ == '__main__':
    main()
