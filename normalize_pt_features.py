#!/usr/bin/env python

import gzip
import sys

for linenr, line in enumerate(gzip.open(sys.argv[1])):
    f = map(float, line.split(' ||| ')[2].split())
    if linenr == 0:
        f_min = [0.0 for v in f]
        f_max = [0.0 for v in f]
    f_min = map(min, zip(f, f_min))
    f_max = map(max, zip(f, f_max))

sys.stderr.write(" ".join(map(str,f_min)) + "\n")
sys.stderr.write(" ".join(map(str,f_max)) + "\n")

for linenr, line in enumerate(gzip.open(sys.argv[1])):
    line = line.split(' ||| ')
    f = map(float, line[2].split())
    for fid in range(len(f)):
        if f_max[fid] - f_min[fid] > 0 and f_max[fid] > 1:
            f[fid] = (f[fid] - f_min[fid]) / (f_max[fid] - f_min[fid])
    line[2] = ' '.join(map(str,f))
    print " ||| ".join(line),
