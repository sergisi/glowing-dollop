from src.distribution import Zipf

def calc(acc, len_msgs, k, people):
    if k == 0:
        return 0
    sum = (len_msgs - acc) / people
    return sum + calc(sum, len_msgs - acc, k - 1, people - 1)


def calculate(msgs: int, k: int, people: int):
    """
    It calculates the perfect anonymity in an uniform distribution,
    having an constant anonymity for all participants of the distribution.
    """
    res = msgs / people
    return res + calc(res, msgs, k - 1, people - 1)

def main():
    print(calculate(len(Zipf(200, 15, 1.3).messages()),4, 200))