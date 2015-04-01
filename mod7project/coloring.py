'''
Created on 30 mrt. 2015

@author: R
'''
from advgraph import graph, vertex
class coloring():
    def __init__(self, G=None):
        if G != None:
            self.partition = {0:set()}
            self.vertexColors = {}
            self.lengths = {0:len(G.V())}
            for V in G.V():
                self.partition[0].add(V)
                self.vertexColors[V] = 0
    
    def __repr__(self):
        return str(self.partition)
    def __getitem__(self, i):
        if type(i) is vertex:
            return self.vertexColors[i];
        if type(i) is int:
            return self.partition[i]
    
    def __setitem__(self, i, value):
        if type(i) is vertex:
            oldColor = self.vertexColors[i]
            self.lengths[oldColor] -= 1
            self.partition[oldColor].remove(i)
            if not self.partition[oldColor]:
                del self.partition[oldColor]
            self.vertexColors[i] = value
            if value in self.partition:
                self.partition[value].add(i)
                self.lengths[value] += 1
            else:
                self.partition[value] = {i}
                self.lengths[value] = 1
        if type(i) is int:
            self.partition[i] = value
            self.lengths[i] = len(value)
            for v in value:
                self.vertexColors[v] = i
    def copy(self):
        result = coloring()
        result.partition = {c:set(self.partition[c]) for c in self.partition}
        result.vertexColors = self.vertexColors.copy()
        result.lengths = self.lengths.copy()
        return result