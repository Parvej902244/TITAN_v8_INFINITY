class ScribeAI:
    def format(self, finding):
        # Enriches finding with readable text
        finding["business_context"] = "High Risk" if finding['severity'] in ["P0", "P1"] else "Low Risk"
        return finding
      
