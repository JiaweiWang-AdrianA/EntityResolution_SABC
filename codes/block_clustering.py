import numpy as np
import itertools
from collections import defaultdict
from sklearn.cluster import KMeans


def jaccardSimilarity(s1, s2):
    ''' Jaccard Similarity
        input: s1(set/list/tuple), s2(set/list/tuple)
        output: Jaccard Similarity between s1 and s2
    '''
    len_union = len(set(s1).union(set(s2)))
    len_inter = len(set(s1)-(set(s1)-set(s2)))
    if len_union != 0:
        res = len_inter/len_union 
    else:
        res = 0
    return res


def calSimMatrixFromBlocks(blocks):
    ''' get the Similarity Matrix from blocks '''
    blocks_num = len(blocks)
    S, matInx2bIds = np.ones((blocks_num, blocks_num)), {}
    bids = list(blocks.keys())
    for i in range(blocks_num):
        for j in range(i+1, blocks_num):
            bid_i, bid_j = bids[i], bids[j]
            matInx2bIds[i], matInx2bIds[j]  = bid_i, bid_j
            block_i, block_j = blocks[bid_i], blocks[bid_j]
            S[i][j] = jaccardSimilarity(block_i, block_j)
            S[j][i] = S[i][j]
    return S, matInx2bIds


def genSimMatrixFromSimOrgMatrix(S_org, sim_method='KNN', param=None):
    ''' generate similarity matrix of graph from original matrix by different methods
        output: similarity matrix of graph
    '''
    N = len(S_org)
    S = np.zeros((N,N))
    # Full Connection
    if sim_method == 'Full':
        S = S_org
    # E-Neighbors
    elif sim_method == 'ENbrs':
        e = param if param else 0.5
        for i in range(N):
            for j in range(i, N):
                S[i][j] = e if S_org[i][j] >= e else 0
                S[j][i] = S[i][j]
    # KNN
    else: 
        k = param if param else 4
        for i in range(N):
            dist_with_index = zip(S_org[i], range(N))
            dist_with_index = sorted(dist_with_index, key=lambda x:x[0], reverse=True)
            nbrs_id = [dist_with_index[m][1] for m in range(min(k+1,N))] 
            #print(str(i)+':'+str(nbrs_id))
            for j in nbrs_id:
                S[i][j] = S_org[i][j] if i != j else 0
        # Averaging to generate symmetric matrix
        S = (S+S.T)/2
        #print(S)
    return S

def calLaplacianMatrix_RCUT(simMatrix):
    ''' calculate Laplacian Matrix using RatioCut
        output: Laplacian Matrix
    '''
    # compute the Degree Matrix: D=sum(A)
    degreeMatrix = np.sum(simMatrix, axis=1)
    # compute the Laplacian Matrix: L=D-A
    laplacianMatrix = np.diag(degreeMatrix) - simMatrix #np.diag:以一维数组的形式返回方阵的对角线
    # print degreeMatrix
    # pirnt(degreeMatrix)
    return np.nan_to_num(laplacianMatrix)

def calLaplacianMatrix_NCUT(simMatrix):
    ''' calculate Laplacian Matrix using NCut
        output: Normalized Laplacian Matrix
    '''
    # compute the Degree Matrix: D=sum(A)
    degreeMatrix = np.sum(simMatrix, axis=1)
    # compute the Laplacian Matrix: L=D-A
    laplacianMatrix = np.diag(degreeMatrix) - simMatrix #np.diag:以一维数组的形式返回方阵的对角线
    # normailze: n_L = D^(-1/2) L D^(-1/2)
    np.seterr(divide='ignore', invalid='ignore')
    sqrtDegreeMatrix = np.diag(1.0 / (degreeMatrix ** (0.5)))
    n_laplacianMatrix = np.dot(np.dot(sqrtDegreeMatrix, laplacianMatrix), sqrtDegreeMatrix)
    return np.nan_to_num(n_laplacianMatrix)


def calOptimalIndicatorByKMeans(simMatrix, cut_method='NCut', cluster_num=2, k=None):
    ''' calculate Optimal Indicator Vector by k-means
        output: optimal cut solution
    '''
    if cut_method == 'RCut':
        Laplacian = calLaplacianMatrix_RCUT(simMatrix)
    else:
        Laplacian = calLaplacianMatrix_NCUT(simMatrix)
    if not k:
        k = cluster_num
    x, V = np.linalg.eig(Laplacian)
    x = zip(x, range(len(x)))
    x = sorted(x, key=lambda x: x[0])
    H = np.vstack([V[:, i] for (v, i) in x[:k]]).T
    if(isinstance(H[0][0],complex)):
        H = abs(H)
    optH_kmeans = KMeans(n_clusters=cluster_num).fit(H)
    return optH_kmeans


def specralClustering(blocks, cluster_num=1, sim_method='KNN', sim_param=None, cut_method='NCut', cut_k=None):
    """
            input:	blocks, cluster_num
            output:	a dictionary(new blocks)
    """
    blocks_res = defaultdict(set)
    S_org, matInx2bIds = calSimMatrixFromBlocks(blocks)
    #print("S_g:", S_g)
    S = genSimMatrixFromSimOrgMatrix(S_org, sim_method=sim_method, param=sim_param)
    #print("S:", S)
    sp_kmeans = calOptimalIndicatorByKMeans(S, cut_method=cut_method, cluster_num=cluster_num, k=cut_k)
    for i in range(len(S)):
        bid = matInx2bIds[i]
        cid = sp_kmeans.labels_[i]
        for pid in blocks[bid].split(','):
            blocks_res[cid].add(pid)
    for cid in blocks_res.keys():
        blocks_res[cid] = ','.join(blocks_res[cid])
    #print(" cluster result: ", blocks_res)
    return blocks_res
