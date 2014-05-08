#!/usr/bin/python

import sys
import locale
locale.setlocale(locale.LC_ALL, "C") # this is how the PT were sorted

class PTReader(object):
    def __init__(self, filename):
        self.d = open(filename)

    def read(self):
        """ return lines with same left side in batches """
        buffer = []
        for line in self.d:
            line = line.split('|')
            left = line[0].strip()
            right = line[1].strip()
            scores = line[2].strip()
            if buffer and buffer[-1][0] != left:
                yield buffer
                buffer = []
            buffer.append( (left, right, scores) )
        if buffer:
            yield buffer


def combine(buffer_swapped, buffer_backward):
    for pivot_forward, src, scores_forward in buffer_swapped:
        for pivot_backward, para, scores_para in buffer_backward:
            assert locale.strcoll(pivot_forward, pivot_backward) == 0
            # maybe combine scores here
            print "%s ||| %s ||| %s ||| %s" %(src, para, scores_forward, scores_para)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('swapped', help="forward pt mit src/target swapped")
    parser.add_argument('backward', help="backward translation pt")
    args = parser.parse_args(sys.argv[1:])

    swapped_pt = PTReader(args.swapped)
    backward_pt = PTReader(args.backward)

    swapped_iter = swapped_pt.read()
    backward_iter = backward_pt.read()

    buffer_swapped = swapped_iter.next()
    buffer_backward = backward_iter.next()

    try:
        while True:
            left_forward = buffer_swapped[0][0]
            left_backward = buffer_backward[0][0]

            c = locale.strcoll(left_forward, left_backward)
            if c < 0: # swapped PT side is behind
                buffer_swapped = swapped_iter.next()
            elif c > 0: # backward PT is behind
                buffer_backward = backward_iter.next()
            else: # both sides match
                assert c == 0, "%s" %c
                combine(buffer_swapped, buffer_backward)
                buffer_swapped = swapped_iter.next()
                buffer_backward = backward_iter.next()
    except StopIteration:
        pass
