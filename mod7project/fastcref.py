'''
Created on 18 feb. 2015
http://www.automata.rwth-aachen.de/~grohe/pub/berbongro13.pdf
@author: R
'''
from advgraph import graph
from graphIO import loadgraph, writeDOT
import cProfile
from basicdll import DLL
from coloring import coloring
pr = cProfile.Profile()
def sort(data):
    """merge sort in gesorteerde lijst"""
    if len(data) <= 1:
        return list(data)
    else:
        f = list(sort(data[:(len(data) // 2)]))
        s = list(sort(data[(len(data) // 2):]))
        r = []
        fi = 0
        si = 0
        while fi < len(f) and si < len(s):
            if f[fi] < s[si]:
                r.append(f[fi])
                fi = fi + 1
            else:
                r.append(s[si])
                si = si + 1
        if fi < len(f):
            r.extend(f[fi:])
        elif si < len(s):
            r.extend(s[si:])
        return r

def fastColoring(G, C=None, S=None):
    if C == None or S == None:
        C = coloring(G)
        S = DLL([0])
    C = C.copy()
    usedSets = set()
    while not S.isempty():
        cdeg = {}
        r = S.pop()
        R = set(C[r])
        Cadj = {}
        maxcdeg = {}
        for v in R:
            for w in v.nbs():
                deg = (cdeg[w] if w in cdeg else 0) + 1
                cdeg[w] = deg
                c = C[w]
                if c in Cadj:
                    maxcdeg[c] = max(deg, maxcdeg[c])
                    Cadj[c].add(w)
                else:
                    maxcdeg[c] = 1
                    Cadj[c] = {w}
        mincdeg = {}
        Csplit = []
        for i in Cadj:
            if len(Cadj[i]) < C.lengths[i]:
                mincdeg[i] = 0
            else:
                mincdeg[i] = min({cdeg[v] for v in Cadj[i]})
            if mincdeg[i] < maxcdeg[i]:
                Csplit.append(i)
        Csplit = sort(Csplit)
        for s in Csplit:
            numcdeg = [0] * (maxcdeg[s] + 1)
            numcdeg[0] = C.lengths[s] - len(Cadj[s])
            for v in Cadj[s]:
                numcdeg[cdeg[v]] += 1
            bigcolor = -1
            bigcolornum = -1
            i = 0
            j = 0
            newcol = [-1] * (1 + maxcdeg[s])
            numColors = len(C.partition)
            for num in numcdeg:
                if bigcolornum < num:
                    bigcolor = i
                    bigcolornum = num
                if num > 0:
                    if j == 0:
                        newcol[i] = s
                    else:
                        newcol[i] = j - 1 + numColors
                    j += 1
                i += 1
            tup = (s, C.lengths[s])
            for v in Cadj[s]:
                C[v] = newcol[cdeg[v]]
            if tup in usedSets:
                newcol[bigcolor] = -1
            usedSets.add(tup)
            for num in newcol:
                if num >= 0:
                    S.append(num)
    return C


def countIsoMorphism(G1, G2, C1, C2):
    if len(G1.V()) != len(G2.V()) or len(G1.E()) != len(G2.E()):
        return 0
    if C1.lengths != C1.lengths:
        return 0
    if max(C1.lengths.values()) == 1:
        return 1
    c = chooseColorClass(C1.lengths)
    x = chooseVertex(C1, c)
    num = 0
    newC = len(C1.partition)
    C1[x] = newC
    C1x = fastColoring(G1, C1, DLL([newC]))
    C1[x] = c
    ys = C2[c].copy()
    for y in ys:
        C2[y] = newC
        num += countIsoMorphism(G1, G2, C1x, fastColoring(G2, C2, DLL([newC])))
        C2[y] = c
    return num 
    

def chooseVertex(C, color):
    # reason why I did it this way:
    # http://stackoverflow.com/a/1612654
    for v in C[color]:
        break
    return v
def chooseColorClass(LP):
    for c in LP:
        if LP[c] >= 2:
            return c
    return None
    
def test():
    g1 = graph(8)
    g1.addedge(g1[0], g1[1])
    g1.addedge(g1[0], g1[2])
    g1.addedge(g1[0], g1[5])
    g1.addedge(g1[0], g1[7])
    g1.addedge(g1[1], g1[4])
    g1.addedge(g1[1], g1[7])
    g1.addedge(g1[1], g1[6])
    g1.addedge(g1[2], g1[4])
    g1.addedge(g1[3], g1[4])
    g2 = graph(8)
    g2.addedge(g2[7], g2[0])
    g2.addedge(g2[7], g2[1])
    g2.addedge(g2[7], g2[4])
    g2.addedge(g2[7], g2[6])
    g2.addedge(g2[0], g2[3])
    g2.addedge(g2[0], g2[6])
    g2.addedge(g2[0], g2[5])
    g2.addedge(g2[1], g2[3])
    g2.addedge(g2[2], g2[3])
    print(countIsoMorphism(g1, g2, fastColoring(g1, g2)))
def test2():
    gs = loadgraph("bigtrees1.grl", readlist=True)[0]
    print("graph loaded")
    import time
    start = time.time()
    g1 = gs[0]
    g2 = gs[2]
    print(countIsoMorphism(g1, g2, fastColoring(g1), fastColoring(g2)))
    print(time.time() - start)
cProfile.run('test2()', sort='cumtime')
