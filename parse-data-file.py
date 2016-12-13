import re
from collections import namedtuple
from pathlib import Path
from collections import Counter
from operator import attrgetter


Record = namedtuple('Record', 'strategy, num, arena, seed, result')

PATTERN = re.compile(r'Result = (\d+)')


def parse(filename):
    assert isinstance(filename, Path)

    strategy, num, arena, seed = filename.stem.split('_')

    with filename.open() as f:
        match = re.search(PATTERN, f.read())

        result = match.group(1) if match else 0

    return Record(strategy, int(num), arena, int(seed), int(result))


def aggregate(records, field):
    getter = attrgetter(field)
    d = Counter(getter(record) for record in records)
    return d


def findfiles(pattern='**/*.txt', source_dir='.'):
    return Path(source_dir).glob(pattern)


if __name__ == '__main__':
    records = (parse(f) for f in findfiles())

    arenas = aggregate(records, 'arena')
    strategies = aggregate(records, 'strategy')

    print(arenas)
    assert arenas == {'Chigago': 2, 'michigan': 1, 'newOrleans': 3, 'newYork': 4}
    assert strategies == {'buy': 2, 'give': 1, 'sell': 4, 'trade': 3}
