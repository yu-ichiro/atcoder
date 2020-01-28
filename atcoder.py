import json
import sys
from io import StringIO, TextIOWrapper
from multiprocessing import Process, Manager
from tempfile import NamedTemporaryFile
from typing import List, Dict


def run(case_file, func):
    cases: List[Dict] = json.load(case_file)
    for case in cases:
        if set(case.keys()) != {'input', 'output'}:
            continue

        _stdin, _stdout = sys.stdin, sys.stdout
        sys.stdin, sys.stdout = StringIO(case['input']), StringIO()
        func()
        sys.stdout.seek(0)
        out = sys.stdout.read()
        sys.stdin, sys.stdout = _stdin, _stdout

        if out == case['output']:
            print('AC')
        else:
            print('WA')
            print('expected:')
            print(repr(case['output']))
            print('got:')
            print(repr(out))


def run_interactive(case_func, func):
    g = Manager().Namespace()

    file_a = NamedTemporaryFile()
    file_b = NamedTemporaryFile()
    g.file_a = file_a.name
    g.file_b = file_b.name
    g.success = None
    g.error = ''

    def case_wrapper(_case):
        def inner():
            with open(g.file_a, 'a') as _file_a, open(g.file_b) as _file_b:
                _stdin, _stdout = sys.stdin, sys.stdout
                sys.stdin, sys.stdout = _file_b, _file_a
                result = _case()
                sys.stdin, sys.stdout = _stdin, _stdout
                if result is True:
                    g.success = True
                else:
                    g.success = False
                    g.error = result
        return inner

    def func_wrapper(_func):
        def inner():
            with open(g.file_a) as _file_a, open(g.file_b, 'a') as _file_b:
                _stdin, _stdout = sys.stdin, sys.stdout
                sys.stdin, sys.stdout = _file_a, _file_b
                _func()
            sys.stdin, sys.stdout = _stdin, _stdout
        return inner

    case_process = Process(target=case_wrapper(case_func))
    func_process = Process(target=func_wrapper(func))

    case_process.start()
    func_process.start()

    case_process.join()
    func_process.join()

    if g.success:
        print('AC')
    else:
        print('WA')
        print(g.error)
        file_a.seek(0)
        file_b.seek(0)
        print('input:')
        print(TextIOWrapper(file_a).read())
        print('output:')
        print(TextIOWrapper(file_b).read())

    file_a.close()
    file_b.close()


def wait_input(*args, **kwargs):
    try:
        return input(*args, **kwargs)
    except EOFError:
        return wait_input(*args, **kwargs)
