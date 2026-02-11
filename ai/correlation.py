class CorrelationAI:
    def __init__(self):
        self.param_map = {}

    def ingest(self, url, params):
        for k, v in params.items():
            if k not in self.param_map: self.param_map[k] = []
            self.param_map[k].append(url)
            
    def find_reused_ids(self, param):
        return self.param_map.get(param, [])
      
