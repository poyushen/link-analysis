#!/usr/bin/env python3
import numpy as np
import time
from math import sqrt

class HITS():
    def __init__(self, file=None, max_iter=100, tol=1e-6, **kwargs):
        self.graph, self.items = load(file)
        self.max_iter = max_iter
        self.tol = tol
        self.n = len(self.graph)
        self.hubs = [1] * self.n
        self.auth = [1] * self.n

    def hits(self):
        for i in range(self.max_iter):
            prevhubs = sum(self.hubs)
            prevauth = sum(self.auth)

            self.auth = np.matmul(np.array(self.graph).transpose(), np.array(self.hubs))
            auth_scale = sqrt(sum([x**2 for x in self.auth]))

            self.hubs = np.matmul(np.array(self.graph), np.array(self.auth))
            hubs_scale = sqrt(sum([x**2 for x in self.hubs]))

            self.auth = [x / auth_scale for x in self.auth]
            self.hubs = [x / hubs_scale for x in self.hubs]

            if abs(sum(self.hubs) - prevhubs) < self.n * self.tol or abs(sum(self.auth) - prevauth) < self.n*self.tol:
                end = i
                break

        hubs = {self.items[i]:self.hubs[i] for i in range(self.n)}
        auth = {self.items[i]:self.auth[i] for i in range(self.n)}

        return hubs, auth, end

class PageRank():
    def __init__(self, file=None, alpha=0.85, max_iter=100, tol=1e-6, **kwargs):
        self.graph, self.items = load(file)
        self.max_iter = max_iter
        self.tol = tol
        self.n = len(self.graph)
        self.alpha = alpha
        self.pagerank = [1/self.n] * self.n
        self.L = [0] * self.n

    def pr(self):
        for i in range(self.n):
            self.L[i] = sum(self.graph[i])
        for i in range(self.max_iter):
            prevpagerank = sum(self.pagerank)
            for j in range(self.n):
                self.pagerank[j] = 0
                for k in range(self.n):
                    if self.graph[j][k] == 1:
                        self.pagerank[j] = self.pagerank[j] + self.pagerank[k]/self.L[k] if self.L[k] else 1/self.n
                self.pagerank[j] = (1-self.alpha)/self.n + self.alpha*self.pagerank[j]

            if abs(sum(self.pagerank) - prevpagerank) < self.n * self.tol:
                end = i
                break

        pagerank = {self.items[i]:self.pagerank[i] for i in range(self.n)}
        return pagerank, end

def load(path):
    A = []
    items = []
    link = {}
    with open(path) as f:
        for line in f:
            l = [int(i) for i in line.split(',')]
            if l[0] not in link.keys():
                link[l[0]] = []
            link[l[0]].append(l[1])

            if l[0] not in items:
                items.append(l[0])
            if l[1] not in items:
                items.append(l[1])

    items = sorted(items)

    for i in range(len(items)):
        A.append([0] * len(items))
        try:
            for j in link[items[i]]:
                A[i][items.index(j)] = 1
        except:
            A[i] = A[i]

    return A, items

if '__main__' == __name__:
    np.set_printoptions(suppress=True)
    for i in range(1, 9):
        h = HITS(file='data/graph_%d.txt' %i)
        p = PageRank(file='data/graph_%d.txt' %i)
        time1 = time.time()
        hubs, auth, end_h = h.hits()
        time2 = time.time()
        pagerank, end_p = p.pr()
        time3 = time.time()
        with open('result/hits/graph_%d.txt' %i, 'w') as f:
            f.write('\nGraph %d\n' %i)
            f.write('Run %d iterations\n' %end_h)
            f.write('hubs:\n')
            f.write(str(hubs))
            f.write('\nauth:\n')
            f.write(str(auth))

        with open('result/pagerank/graph_%d.txt' %i, 'w') as f:
            f.write('\nGraph %d\n' %i)
            f.write('Run %d iterations\n' %end_p)
            f.write('pagerank:\n')
            f.write(str(pagerank))
