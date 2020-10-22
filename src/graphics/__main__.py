from collections import Counter, defaultdict

import matplotlib.pyplot as plt
from src.zipf import zipf


def show_dist(msgs):
    people = count_people(msgs)
    fig, ax = plt.subplots()
    ax.bar(list(people.keys()), people.values())
    ax.set_xlabel('Number of messages')
    ax.set_ylabel('Number of people')
    ax.set_title(f'Histogram of s: {s}')
    fig.tight_layout()
    plt.savefig(f'histogram-{s}.png')


def count_people(msgs):
    counter = Counter(msgs).most_common()
    num_people = defaultdict(int)
    for num_person, msg_per in counter:
        num_people[msg_per] += 1
    return num_people


if __name__ == '__main__':
    num_msgs = 200
    max_num_msg = 15
    s_range = map(lambda x: x / 10, range(13, 21))
    for s in s_range:
        msgs = zipf(num_msgs, max_num_msg, s)
        show_dist(msgs)
