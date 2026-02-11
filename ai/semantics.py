import re
class SemanticAI:
    def classify(self, params):
        types = {}
        for k, v in params.items():
            if re.search(r"id|uid", k): types[k] = "IDENTITY"
            elif re.search(r"price|amount|balance", k): types[k] = "MONEY"
            elif re.search(r"role|status|admin", k): types[k] = "STATE"
            else: types[k] = "GENERIC"
        return types
      
