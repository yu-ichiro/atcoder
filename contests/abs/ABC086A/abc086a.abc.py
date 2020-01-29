import os

from atcoder import run


def program():
    a, b = map(int, input().split())
    print('Odd' if a % 2 and b % 2 else 'Even')


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'case.json')) as case:
        run(case, program)
