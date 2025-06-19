from z3 import *

def inicializar(n,m,T):
    P = [[[Bool(f"P_{i}_{j}_{t}") for t in range(T+1)] for j in range(m)] for i in range(n)]
    C = [[[Bool(f"C_{i}_{j}_{t}") for t in range(T+1)] for j in range(m)] for i in range(n)]
    M = [[Bool(f"M_{i}_{j}") for j in range(m)] for i in range(n)]
    W = [[Bool(f"W_{i}_{j}") for j in range(m)] for i in range(n)]
    return Solver(), P, C, M, W

