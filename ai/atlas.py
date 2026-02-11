class AtlasAI:
    def __init__(self, config, neg_mem):
        self.config = config
        self.neg_mem = neg_mem
        self.phase = "INIT"
        self.queue = []
        self.stagnation = 0

    def load_state(self, state):
        if state:
            self.phase = state.get("phase", "INIT")
            self.queue = state.get("queue", [])

    def get_state(self):
        return {"phase": self.phase, "queue": self.queue}

    def plan_next_step(self, context):
        # Stagnation Logic Fix
        if context.get("new_endpoints", 0) == 0 and context.get("new_bugs", 0) == 0:
            self.stagnation += 1
        else:
            self.stagnation = 0

        if self.phase != "INIT" and self.stagnation > self.config['ai']['stagnation_limit']:
            return ["FINALIZE"]

        if not self.queue:
            if self.phase == "INIT":
                self.phase = "DISCOVERY"
                return ["ORION_DISCOVERY"]
            elif self.phase == "DISCOVERY":
                self.phase = "LOGIC_MAPPING"
                return ["LOGOS_ANALYSIS"]
            
        return self.queue.pop(0) if self.queue else ["WAIT"]
      
