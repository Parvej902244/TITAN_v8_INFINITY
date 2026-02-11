class EvidenceChain:
    def __init__(self):
        self.steps = []
        self.confidence = 0

    def add_evidence(self, step, desc, boost):
        self.steps.append(f"[{step}] {desc} (+{boost}%)")
        self.confidence = min(100, self.confidence + boost)

    def penalize(self, reason, penalty):
        self.steps.append(f"[PENALTY] {reason} (-{penalty}%)")
        self.confidence = max(0, self.confidence - penalty)

    def get_explanation(self):
        return "\n".join(self.steps)
      
