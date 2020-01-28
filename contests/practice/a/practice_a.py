import os.path

from atcoder import run


def program():
    a = int(input())
    b, c = map(int, input().split())
    s = input()
    print(a+b+c, s)


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'case.json')) as case:
        run(case, program)
