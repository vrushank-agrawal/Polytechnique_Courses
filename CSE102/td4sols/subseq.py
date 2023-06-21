"""Subsequences."""

def subseq(seq):
    if seq == []:
        yield []
    else:
        for s in subseq(seq[1:]):
            yield s
            yield [seq[0]] + s
