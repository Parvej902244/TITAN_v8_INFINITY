import json
import os

class GlobalExperienceMemory:
    def __init__(self):
        self.file = "global_patterns.json"
        self.patterns = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file) as f: return json.load(f)
        return {"vuln_params": [], "safe_paths": []}

    def learn_vuln_param(self, param):
        if param not in self.patterns["vuln_params"]:
            self.patterns["vuln_params"].append(param)
            self.save()

    def save(self):
        with open(self.file, "w") as f: json.dump(self.patterns, f)
          
