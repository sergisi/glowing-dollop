from typing import Union, Tuple


class Line:

    def __init__(self, k: Union[str, int], values: Tuple[float]):
        self.k: int = k
        self.values = values

    def show(self):
        print(f'{self.k} & ' + ' & '.join(str(self.values)[1:-1].split(', ')) + r'\\')
