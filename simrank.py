from graph import graph
import numpy as np
import time
from pprint import PrettyPrinter

def simrank(graph, min_diff=0.01, decay_factor=0.8):
    nodes = graph.nodes()
    sim = np.identity(len(nodes))
    iteration = 0

    while True:
        iteration += 1
        prev_sim = np.copy(sim)

        for idx_u, u in enumerate(nodes):
            for idx_v, v in enumerate(nodes):
                if u is v:
                    continue

                len_up = len(graph.parents(u))
                len_vp = len(graph.parents(v))
                if len_up == 0 or len_vp == 0:
                    sim[idx_u][idx_v] = 0
                else:
                    sum = 0
                    for u_p in graph.parents(u):
                        for v_p in graph.parents(v):
                            sum += prev_sim[nodes.index(u_p)][nodes.index(v_p)]
                    sim[idx_u][idx_v] = (decay_factor / (len_up * len_vp)) * sum

        if np.allclose(sim, prev_sim, atol=min_diff):
            break

    return sim, iteration

if __name__ == '__main__':

    graphs = list()
    for i in range(1, 7):
        from graph import graph
        filename = 'data/graph_{}.txt'.format(i)
        graph = graph()
        graph.read_from_file(filename)
        graphs.append(graph)


    for idx, graph in enumerate(graphs, 1):
        time1 = time.time()
        if idx == 6:
            break

        filename = 'graph_{}.txt'.format(idx)
        with open(filename, 'w') as f:
            pp = PrettyPrinter(indent=4, stream=f)
            f.write('\nGraph {}\n'.format(idx))
            s, i = simrank(graph)
            f.write('Run {} iterations \nSimRank:\n'.format(i))
            pp.pprint(s)
        time2 = time.time()
        print("graph_%d: "%idx, time2-time1)
    print('end')
