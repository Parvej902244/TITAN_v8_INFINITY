class SpectrumAI:
    def __init__(self):
        self.discovered = set()
        self.analyzed = set()
    
    def add_discovered(self, eps):
        self.discovered.update(eps)
        
    def add_analyzed(self, ep):
        self.analyzed.add(ep)
        
    def get_stats(self):
        return len(self.discovered), len(self.analyzed)

    def is_complete(self):
        if not self.discovered: return False
        return (len(self.analyzed) / len(self.discovered)) > 0.95
      
