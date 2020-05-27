import sys
from typing import Union, Tuple, List


class Line:

    def __init__(self, k: Union[str, int], values: Tuple[float]):
        self.k: int = k
        self.values = values

    def show(self):
        print(f'{self.k} & ' + ' & '.join(str(self.values)[1:-1].split(', ')) + r'\\')


def table(func):
    def wrapper(*args, **kwargs):
        print(r"\begin{table}[H]", file=file)
        func(*args, **kwargs)
        print(r"\end{table}", file=file)

    return wrapper


def tabular(ncols: f'{self.k} & ' + ' & '.join(str(self.values)[1:-1].split(', ')) + r'\\'int, text):
    cols = u'|'.join("c" for _ in range(ncols))
    print(r'\begin{tabular}{' + f'{cols}' + '}')
    print(text)
    print(r'\end{tabular}')


def show_tables():
    for line in file:
        if line.startswith('S'):
            print(r"\begin{table}[H]", file=file)
            tabular(1, f"k: {line[3:-1]}")
            print(r"\end{table}", file=file)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python -m src.texparser <out file>")
        sys.exit()
    with open(sys.argv[1]) as file:
        show_tables()