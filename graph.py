import re
from xml.dom.minidom import Document, parseString

class graph():
    def __init__(self):
        self.node_ch = {}
        self.node_pa = {}


    def nodes(self):
        return list(self.node_ch.keys())


    def edges(self):
        return [ a for a in self._edges() ]


    def _edges(self):
        for n, childs in self.node_ch.items():
            for child in childs:
                yield (n, child)


    def childrens(self, node):
        return self.node_ch[node]


    def parents(self, node):
        return self.node_pa[node]


    def has_node(self, node):
        return node in self.node_ch


    def add_node(self, node):
        if node not in self.node_ch:
            self.node_ch[node] = list()
            self.node_pa[node] = list()


    def add_edge(self, edge):
        u, v = edge
        if v in self.node_ch[u] and u in self.node_pa[v]:
            #print('Edge exist!')
            pass
        else:
            self.node_ch[u].append(v)
            self.node_pa[v].append(u)


    def read_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                match = re.match('(\d+),(\d+)', line)
                if match:
                    u, v = match.groups()
                    self.add_node(u)
                    self.add_node(v)
                    self.add_edge((u, v))
