class CriticusAI:
    def validate(self, finding):
        if finding['severity'] in ["P0", "P1"] and finding['confidence'] < 80:
            finding['severity'] = "P2"
            finding['validation_notes'] = "Downgraded due to low confidence."
        return True
      
