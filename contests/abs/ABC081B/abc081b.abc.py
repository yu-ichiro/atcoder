import os.path

from atcoder import run


def program():
    _ = int(input())
    args = list(map(int, input().split()))
    div = 0
    while all(map(lambda a: a % 2**div == 0, args)):
        div += 1
    print(div-1)


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'case.json')) as case:
        run(case, program)
