#!/usr/bin/env python

import sys
import re
from collections import defaultdict
from itertools import imap, izip

# [PRN] ||| -lrb- [VBN,1] [-RRB-,2] osman ertug ||| -lrb- [VBN,1] [-RRB-,2] osman ertu ||| Abstract=0 Adjacent=1 CharCountDiff=-1 CharLogCR=-0.05407 ContainsX=0 GlueRule=0 Identity=0 Lex(e|f)=62.61372 Lex(f|e)=62.61372 Lexical=0 LogCount=0.69315 Monotonic=1 PhrasePenalty=1 RarityPenalty=0 SourceTerminalsButNoTarget=0 SourceWords=3 TargetTerminalsButNoSource=0 TargetWords=3 UnalignedSource=0 UnalignedTarget=0 WordCountDiff=0 WordLenDiff=-0.33333 WordLogCR=0 p(LHS|e)=0.36291 p(LHS|f)=0.74194 p(e|LHS)=15.18701 p(e|f)=-0.00425 p(e|f,LHS)=-0.00425 p(f|LHS)=15.27798 p(f|e)=0.00431 p(f|e,LHS)=0.00431 AGigaSim=0.75951 GoogleNgramSim=0.68302 ||| 0-0 1-1 2-2 3-3 4-4

def is_nonterminal(s):
    return s.startswith('[') and s.endswith(']')

def fix_align(align, lhs, rhs):
    res = []
    lh_term = map(is_nonterminal, lhs.split())
    rh_term = map(is_nonterminal, rhs.split())
    for a in align.split():
        l, r = map(int, a.split('-'))
        #if not lh_term[l] == rh_term[r]:
        #    print align, lhs, rhs
        #assert lh_term[l] == rh_term[r]
        if lh_term[l] and rh_term[r]:
            res.append("%d-%d" %(l,r))

    return " ".join(res)

def process(line):
    line = re.sub(r'\[[^\]]+\]', '[X][X]', line)
    line = [elem.strip() for elem in line.split('|||')][1:]
    features = line[2].split()
    feature_values = [v for n,v in [f.split('=') for f in features]]
    return ' ||| '.join(["%s [X]" %line[0],
                         "%s [X]" %line[1],
                         " ".join(feature_values),
                         fix_align(line[3],line[0],line[1]),
                         "0 0 0"])

if __name__ == "__main__":

    for linenr, line in enumerate(sys.stdin):
        line = line.strip()
        print process(line)
