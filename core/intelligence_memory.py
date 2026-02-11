class IntelligenceMemory:
    def __init__(self):
        self.analyzed_endpoints = set()
        self.bug_types_found = set()

    def mark_analyzed(self, ep):
        self.analyzed_endpoints.add(ep)

    def is_analyzed(self, ep):
        return ep in self.analyzed_endpoints

    def record_bug(self, btype):
        self.bug_types_found.add(btype)
      
