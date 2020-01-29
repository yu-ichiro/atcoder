import random

from atcoder import run_interactive


def program():
    letter_count, limit = map(int, input().split())
    table = list(map(chr, range(ord('A'), ord('A') + letter_count)))

    def judge(a, b):
        print('?', a, b, flush=True)
        result = input().strip()
        return -1 if result == '<' else 1

    def quick_sort(_table):
        if len(_table) <= 1:
            return _table
        pivot = _table[len(_table)//2]
        left = []
        right = []
        for item in _table:
            if item == pivot:
                continue
            if judge(item, pivot) == -1:
                left.append(item)
            else:
                right.append(item)
        return quick_sort(left) + [pivot] + quick_sort(right)

    print('!', ''.join(quick_sort(table)), flush=True)


def generate_case(letter_count, limit):
    def case():
        table = list(map(chr, range(ord('A'), ord('A') + letter_count)))
        random.shuffle(table)
        answer = ''.join(table)
        print(letter_count, limit, flush=True)

        def judge(a, b):
            if not {a, b}.issubset(table):
                return '?'
            if a == b:
                return '='
            a_idx = table.index(a)
            b_idx = table.index(b)
            return '<' if a_idx < b_idx else '>'

        for i in range(limit):
            query = input().split()
            if query[0] == '?':
                print(judge(*query[1:]), flush=True)
            elif query[0] == '!':
                output = query[1]
                break
            else:
                print('?', flush=True)
        else:
            return 'Time up'

        if answer == output:
            return True
        else:
            return f'Wrong Answer.\nCorrect: {answer}\nGot: {output}'
    return case


if __name__ == '__main__':
    run_interactive(generate_case(3, 10), program)
    run_interactive(generate_case(26, 1000), program)
    run_interactive(generate_case(26, 100), program)
    run_interactive(generate_case(5, 7), program)
