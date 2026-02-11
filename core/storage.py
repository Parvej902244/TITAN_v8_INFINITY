import os
import json
import hashlib
import logging
from datetime import datetime

class StorageEngine:
    def __init__(self, target: str):
        self.target = target.replace("https://", "").replace("http://", "").strip("/")
        self.base_dir = f"scans/{self.target}"
        self.manifest_file = f"{self.base_dir}/bug_manifest.json"
        self.state_file = f"{self.base_dir}/scan_state.json"
        self.setup_dirs()
        self.load_manifest()

    def setup_dirs(self):
        dirs = ['bugs', 'raw', 'normalized', 'diffs', 'states', 'logs']
        for d in dirs:
            os.makedirs(f"{self.base_dir}/{d}", exist_ok=True)

    def load_manifest(self):
        if os.path.exists(self.manifest_file):
            with open(self.manifest_file, 'r') as f:
                self.bug_hashes = set(json.load(f))
        else:
            self.bug_hashes = set()

    def save_manifest(self):
        with open(self.manifest_file, 'w') as f:
            json.dump(list(self.bug_hashes), f)

    def save_state(self, state_data: dict):
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f)
            
    def load_state(self) -> dict:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}

    def generate_bug_hash(self, bug_data: dict) -> str:
        unique_string = f"{bug_data.get('type')}|{bug_data.get('location')}|{bug_data.get('description')}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def save_bug(self, bug_data: dict):
        bug_hash = self.generate_bug_hash(bug_data)
        if bug_hash in self.bug_hashes: return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bug_id = f"bug_{timestamp}_{bug_data.get('type', 'logic').replace(' ', '_')}"
        filename = f"{self.base_dir}/bugs/{bug_id}.txt"
        
        content = f"""BUG ID: {bug_id}
SEVERITY: {bug_data.get('severity', 'P4')}
CONFIDENCE: {bug_data.get('confidence', 0)}%

WHAT IS THE BUG:
{bug_data.get('description', 'N/A')}

WHERE IT EXISTS:
{bug_data.get('location', 'N/A')}

HOW IT WAS FOUND:
{bug_data.get('discovery_method', 'N/A')}

WHY IT MATTERS:
{bug_data.get('impact', 'N/A')}

HOW TO FIX:
{bug_data.get('remediation', 'N/A')}

EVIDENCE CHAIN:
{bug_data.get('evidence_explanation', 'N/A')}

BUSINESS CONTEXT:
{bug_data.get('business_context', 'General')}
"""
        with open(filename, "w") as f:
            f.write(content)
        
        self.bug_hashes.add(bug_hash)
        self.save_manifest()
        logging.info(f"✅ Bug Saved: {filename}")
      
