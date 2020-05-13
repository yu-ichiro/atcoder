import random
from atcoder import run_interactive


def program():
    from math import log
    from itertools import permutations, combinations
    letter_count, limit = map(int, input().split())
    table = list(map(chr, range(ord('A'), ord('A') + letter_count)))

    def judge(a, b):
        print('?', a, b, flush=True)
        result = input().strip()
        return -1 if result == '<' else 1

    def bin_search_insert_sort(_table):
        _sorted = [_table.pop(0)]

        def extend_sorted(__sorted, _item):
            if not __sorted:
                return [_item]
            pivot = len(__sorted) // 2
            p_item = __sorted[pivot]
            return (
                __sorted[:pivot+1] + extend_sorted(__sorted[pivot+1:], _item) if judge(p_item, _item) == -1 else
                extend_sorted(__sorted[:pivot], _item) + __sorted[pivot:]
            )
        while len(_table) > 0:
            item = _table.pop(0)
            _sorted = extend_sorted(_sorted, item)
        return _sorted

    def min_max(_table):
        p_list = list(permutations(_table))
        c_list = list(combinations(_table, 2))

        def score(_c):
            _score = 0
            for p in p_list:
                if p.index(_c[0]) < p.index(_c[1]):
                    _score += 1
                else:
                    _score -= 1
            return abs(_score)

        while len(c_list) > 0:
            c = min(c_list, key=lambda _c: score(_c))
            a, b = c

            j = judge(a, b)
            if j == 1:
                a, b = b, a

            p_list = list(filter(lambda p: p.index(a) < p.index(b), p_list))
            c_list.remove((c[0], c[1]))
            if len(p_list) == 1:
                break
        return p_list[0]

    print(
        '!',
        ''.join(min_max(table) if limit < letter_count * log(letter_count) else bin_search_insert_sort(table)),
        flush=True
    )


def generate_case(letter_count, limit):
    def case():
        table = list(map(chr, range(ord('A'), ord('A') + letter_count)))
        random.shuffle(table)
        answer = ''.join(table)
        left_count = limit
        print(letter_count, left_count, flush=True)

        def judge(a, b):
            if not {a, b}.issubset(table):
                return '?'
            if a == b:
                return '='
            a_idx = table.index(a)
            b_idx = table.index(b)
            return '<' if a_idx < b_idx else '>'

        while left_count >= 0:
            query = input().split()
            if query[0] == '?':
                left_count -= 1
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
