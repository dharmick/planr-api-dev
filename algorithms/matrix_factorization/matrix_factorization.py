""" INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
    OUTPUT:
    the final matrices P and Q
"""
import numpy as np
import collections
import json

# import pandas as pd
# import csv

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = np.dot(P,Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
    return P, Q.T


def run_matrix_factorization(user_poi_ratings_matrix):

    R = user_poi_ratings_matrix
    # reader = csv.reader(open("user_poi.csv", "rb"), delimiter=",")
    # x = list(reader)
    # result = np.array(x).astype("float")
    # print(result)

    # data_all = np.loadtxt(open("user_poi - _.csv", "rb"), dtype=np.str, delimiter=",")

    # user_ids = data_all[1:, 0]
    # poi_ids = data_all[0, 2:]

    # data = np.delete(data_all, 0, axis=0)
    # data = np.delete(data, [0,1], axis=1)

    # data[data=='']='0'

    # R = data.astype(np.float)

    # print(R)
    # print(R)

    """for i in range(len(R)):
        print('user', i+1)
        print(R[i])
        print()"""

    # R = [
    #      [5,0,0,1],
    #      [4,0,0,1],
    #      [0,1,0,5],
    #      [1,0,0,4],
    #      [0,1,5,0],
    #     ]

    # R = np.array(R)

    N = len(R)
    M = len(R[0])
    K = 6

    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)


    nP, nQ = matrix_factorization(R, P, Q, K)

    # return np, nQ

    nR = np.dot(nP, nQ.T)
    return nR
    # print(nR)

    # # rating = {
    # #     1: {
    # #         1: 4.2,
    # #         2: 4.5,
    # #     }
    # # }

    # rui_star = {}


    # for i in range(len(nR)):
    #         rui_star[user_ids[i]] = {}
    #         for j in range(len(nR[i])):
    #             # print(i, j)
    #             rui_star[user_ids[i]][poi_ids[j]] = nR[i][j]


    # # sorted_x = dict(sorted(rui_star.items(), key=lambda kv: kv[1], reverse=True))
    # # print(rui_star[1])

    # fp = open("rui_star.json","w")
    # json.dump(rui_star, fp)


    # # print(nP)
    # print(rui_star)
    # # print(nQ)
    # print("------------------")

    # print(len(nR))
    # # data = []







    # for i in range(len(nR)):
        # print('poi', i+1)
        # print(nR[i])
        # data.append(nR[i])
        # print()

    # print(type(nR))
    # print("user 1")
    # print(nR[0])
    # data = [nR[0],nR[1]]
    # df = pd.DataFrame(nR)
    # df.index+=1
    # print(df)
    # nR.to_csv('temp.csv')
    # print()
    # print("user 2")
    # print(nR[1])
    # print()
    # print("user 7")
    # print(nR[6])
    # print()
    # print("user 10")
    # print(nR[9])
    # print(Q)