import os.path

from atcoder import run


def program():
    s = input()
    print(s.count('1'))


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'case.json')) as case:
        run(case, program)
