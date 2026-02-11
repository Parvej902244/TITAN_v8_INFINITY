import networkx as nx

class StateGraphEngine:
    def __init__(self):
        self.graph = nx.DiGraph()

    def record_transition(self, from_url, to_url):
        self.graph.add_edge(from_url, to_url)

    def detect_illegal_jump(self, path):
        # path = [url1, url2, url3]
        if len(path) < 2: return []
        anomalies = []
        for i in range(len(path)-1):
            if not self.graph.has_edge(path[i], path[i+1]):
                anomalies.append(f"Jump {path[i]} -> {path[i+1]} without edge")
        return anomalies
      
