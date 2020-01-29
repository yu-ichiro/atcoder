import json
import os
import sys
from io import StringIO, TextIOWrapper
from multiprocessing import Process, Manager
from tempfile import NamedTemporaryFile, TemporaryDirectory
from types import TracebackType
from typing import List, Dict, IO, Optional, Type, AnyStr, Iterator, Iterable


class MultiWriterProxy(IO):
    def __init__(self, *ios):
        self.ios = list(ios)

    def __proxy__(self, func, *args, **kwargs):
        return self.__proxy_all__(func, *args, **kwargs)[-1]

    def __proxy_all__(self, func, *args, **kwargs):
        final_return = []
        for io in self.ios:
            final_return.append(getattr(type(io), func)(io, *args, **kwargs))
        return final_return

    def close(self) -> None:
        self.__proxy__('close')

    def fileno(self) -> int:
        return self.__proxy__('fileno')

    def flush(self) -> None:
        self.__proxy__('flush')

    def isatty(self) -> bool:
        return self.__proxy__('isatty')

    def read(self, n: int = ...) -> AnyStr:
        return self.__proxy__('read', n)

    def readable(self) -> bool:
        return self.__proxy__('readable')

    def readline(self, limit: int = ...) -> AnyStr:
        return self.__proxy__('readline', limit)

    def readlines(self, hint: int = ...) -> List[AnyStr]:
        return self.__proxy__('readlines', hint)

    def seek(self, offset: int, whence: int = ...) -> int:
        return self.__proxy__('seek', offset, whence)

    def seekable(self) -> bool:
        return self.__proxy__('seekable')

    def tell(self) -> int:
        return self.__proxy__('tell')

    def truncate(self, size: Optional[int] = ...) -> int:
        return self.__proxy__('truncate', size)

    def writable(self) -> bool:
        return self.__proxy__('writable')

    def write(self, s: AnyStr) -> int:
        return self.__proxy__('write', s)

    def writelines(self, lines: Iterable[AnyStr]) -> None:
        return self.__proxy__('writelines', lines)

    def __next__(self) -> AnyStr:
        return self.__proxy__('__next__')

    def __iter__(self) -> Iterator[AnyStr]:
        return self

    def __enter__(self) -> IO[AnyStr]:
        self.ios = self.__proxy_all__('__enter__')
        return self

    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        return all(self.__proxy_all__('__exit__', t, value, traceback))


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

    tempdir = TemporaryDirectory()
    g.file_a = os.path.join(tempdir.name, 'a')
    g.file_b = os.path.join(tempdir.name, 'b')
    os.mkfifo(g.file_a)
    os.mkfifo(g.file_b)

    log_file = NamedTemporaryFile()
    g.log = log_file.name

    g.success = None
    g.error = ''

    def func_wrapper(_func):
        def inner():
            with open(g.file_a, 'r') as _file_a, open(g.file_b, 'w') as _file_b, open(g.log, 'a') as log:
                _stdin, _stdout = sys.stdin, sys.stdout
                sys.stdin, sys.stdout = _file_a, MultiWriterProxy(_file_b, log)
                _func()
                sys.stdin, sys.stdout = _stdin, _stdout
        return inner

    def case_wrapper(_case):
        def inner():
            func_process = Process(target=func_wrapper(func))
            func_process.start()
            with open(g.file_a, 'w') as _file_a, open(g.file_b, 'r') as _file_b, open(g.log, 'a') as log:
                _stdin, _stdout = sys.stdin, sys.stdout
                sys.stdin, sys.stdout = _file_b, MultiWriterProxy(_file_a, log)
                result = _case()
                sys.stdin, sys.stdout = _stdin, _stdout
                if result is True:
                    g.success = True
                else:
                    g.success = False
                    g.error = result
                if func_process.is_alive():
                    func_process.kill()
        return inner

    case_process = Process(target=case_wrapper(case_func))

    case_process.start()
    case_process.join()

    if g.success:
        print('AC')
    else:
        print('WA')
        print(g.error)

        log_file.seek(0)
        print('log:')
        print(TextIOWrapper(log_file).read())

    os.unlink(g.file_a)
    os.unlink(g.file_b)
    log_file.close()
    tempdir.cleanup()
