def calc(acc, len_msgs, k, people):
    if k == 0:
        return 0
    sum = (len_msgs - acc) / people
    return sum + calc(sum, len_msgs - acc, k - 1, people - 1)


def calculate(msgs: int, k: int, people: int):
    res = msgs / people
    return res + calc(res, msgs, k - 1, people - 1)
