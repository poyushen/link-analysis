#!/usr/bin/env python3
import numpy as np

tup = []
queries = []
ads = []
with open('./data/graph_4.txt') as f:
    for line in f:
        l = [int(i) for i in line.split(',')]
        tup.append(tuple(l))
        queries.append(l[0])
        ads.append(l[1])

graph = np.matrix(np.zeros([len(queries), len(ads)]))

for l in tup:
    query = l[0]
    ad = l[1]
    q_i = queries.index(query)
    a_j = ads.index(ad)
    graph[q_i, a_j] += 1

query_sim = np.matrix(np.identity(len(queries)))
ad_sim = np.matrix(np.identity(len(ads)))

def get_ads_num(query):
    q_i = queries.index(query)
    return graph[q_i]

def get_queries_num(ad):
    a_j = ads.index(ad)
    return graph.transpose()[a_j]

def get_ads(query):
    series = get_ads_num(query).tolist()[0]
    return [ ads[x] for x in range(len(series)) if series[x] > 0 ]

def get_queries(ad):
    series = get_queries_num(ad).tolist()[0]
    return [ queries[x] for x in range(len(series)) if series[x] > 0 ]


def query_simrank(q1, q2, C):
    if q1 == q2 : return 1
    prefix = C / (get_ads_num(q1).sum() * get_ads_num(q2).sum())
    postfix = 0
    for ad_i in get_ads(q1):
        for ad_j in get_ads(q2):
            i = ads.index(ad_i)
            j = ads.index(ad_j)
            postfix += ad_sim[i, j]
    return prefix * postfix

def ad_simrank(a1, a2, C):
    if a1 == a2 : return 1
    prefix = C / (get_queries_num(a1).sum() * get_queries_num(a2).sum())
    postfix = 0
    for query_i in get_queries(a1):
        for query_j in get_queries(a2):
            i = queries.index(query_i)
            j = queries.index(query_j)
            postfix += query_sim[i,j]
    return prefix * postfix

def simrank(C=0.8, times=1):
    global query_sim, ad_sim

    for run in range(times):
        # queries simrank
        new_query_sim = np.matrix(np.identity(len(queries)))
        for qi in queries:
            for qj in queries:
                i = queries.index(qi)
                j = queries.index(qj)
                new_query_sim[i,j] = query_simrank(qi, qj, C)

        # ads simrank
        new_ad_sim = np.matrix(np.identity(len(ads)))
        for ai in ads:
            for aj in ads:
                i = ads.index(ai)
                j = ads.index(aj)
                new_ad_sim[i,j] = ad_simrank(ai, aj, C)

        query_sim = new_query_sim
        ad_sim = new_ad_sim
    print(query_sim)
    print(ad_sim)

simrank()

