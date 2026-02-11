class RiskOS:
    def evaluate(self, finding):
        severity = "P4"
        conf = finding.get("confidence", 0)
        
        if "IDOR" in finding['type']: severity = "P1"
        if conf > 90 and severity == "P1": severity = "P0"
        
        finding['severity'] = severity
        return finding
      
