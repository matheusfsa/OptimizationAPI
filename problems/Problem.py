class Problem(object):
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def get_upper_lower(self):
        raise NotImplementedError("Should have implemented this")

    def evaluate(self, X):
        raise NotImplementedError("Should have implemented this")