import sys


def table(func):
    def wrapper(*args, **kwargs):
        print(r"\begin{table}[H]", file=file)
        func(*args, **kwargs)
        print(r"\end{table}", file=file)

    return wrapper


@table
def tabular(ncols: int, nrows: int, text):
    cols = u'|'.join("c" for _ in range(ncols))
    print(r'\begin{tabular}{' + f'{cols}' + '}')
    print(text)
    print(r'\end{tabular}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python -m src.texparser <out file>")
        sys.exit()
    with open(sys.argv[1]) as file:
        table()
