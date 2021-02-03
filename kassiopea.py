from scipy.sparse import coo_matrix, triu, linalg
import scipy as sp
from copy import deepcopy

# Kassiopea is a simple network library. This library, contains basic graph algorithms such as node's neighbours,
# node's degrees, and bipartite projection


class Kassiopea:
    def __init__(self):
        self.list_nodes = []
        self.list_edges = []
        self.list_edges_indices = []
        self.zea = []
        self.label = []

        self.C = coo_matrix((1, 1))
        self.node = {}
        self.edges = {}

    def add_node(self, node, zea=None, label=None):
        if node not in self.list_nodes:
            self.list_nodes.append(node)
            self.zea.append(zea)
            self.label.append(label)
            return True
        return False

    def add_edge(self, node1, node2):
        edge = (node1, node2)
        self.list_edges.append(edge)
        self.list_edges_indices.append((self.list_nodes.index(node1), self.list_nodes.index(node2)))

    def edge_indices(self):
        return self.list_edges_indices

    def adj_matrix(self):
        self.edge_indices()

        n = len(self.list_nodes)
        m = len(self.list_edges_indices)

        r = [x for (x, y) in self.list_edges_indices]
        c = [y for (x, y) in self.list_edges_indices]
        d = [1] * m
        B = coo_matrix((d, (r, c)), shape=(n, n), dtype=float)
        return B + B.transpose()

    def projection(self):
        # Adj * Adj = Adj of projection network
        # see: https://en.wikipedia.org/wiki/Bipartite_network_projection
        A = self.adj_matrix()
        P = triu(A * A, k=1)

        self.list_edges_indices = list(tuple(zip(*P.nonzero())))
        self.list_edges = [(self.list_nodes[n1], self.list_nodes[n2]) for (n1, n2) in self.list_edges_indices]

    def neighbors(self, node):
        n = self.list_nodes.index(node)
        C = self.A.tocsr()
        neighbors = C[n].nonzero()
        return [self.list_nodes[i] for i in neighbors[1]]

    def get_C(self):
        # convert adj matrix to scr format
        # see: https://docs.scipy.org/doc/scipy/reference/sparse.html
        self.C = self.adj_matrix().tocsr()

    def degree(self, node):
        n = node
        return int(self.C[n].sum(1))

    def get_edges(self):
        return self.list_edges

    def get_nodes(self):
        return self.list_nodes

    def update_label(self, label):
        self.label = deepcopy(label)

    def update_zea(self, zea):
        self.zea = deepcopy(zea)

    def update_zea_node(self, node, zea):
        self.zea[node] = zea

    def update_label_node(self, node, label):
        self.label[node] = label

    def eigenvector_centrality(self, max_iter=500, tol=0):
        # see: https://en.wikipedia.org/wiki/Eigenvector_centrality
        A = self.adj_matrix()
        eigenvalue, eigenvector = linalg.eigs(A.T, k=1, which='LR', maxiter=max_iter, tol=tol)
        largest = eigenvector.flatten().real
        norm = sp.sign(largest.sum()) * sp.linalg.norm(largest)
        return dict(zip(self.list_nodes, largest / norm))

    def eigenvector_centrality_projected(self, max_iter = 500, tol = 0):
        A = self.adj_matrix()
        P = triu(A * A, k=1)

        eigenvalue, eigenvector = linalg.eigs(P.T, k=1, which='LR', maxiter=max_iter, tol=tol)
        largest = eigenvector.flatten().real
        norm = sp.sign(largest.sum()) * sp.linalg.norm(largest)
        return dict(zip(self.list_nodes, largest / norm))
