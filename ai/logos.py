import json
from bs4 import BeautifulSoup

class LogosAI:
    def get_struct_hash(self, body):
        try:
            return str(sorted(json.loads(body).keys()))
        except:
            return str(len(body))

    def analyze_idor(self, auth_resp, unauth_resp):
        if auth_resp['status'] != 200: return {"is_bug": False}
        
        hash_a = self.get_struct_hash(auth_resp['body'])
        hash_b = self.get_struct_hash(unauth_resp['body'])
        
        if hash_a == hash_b and auth_resp['status'] == unauth_resp['status']:
             return {
                "is_bug": True,
                "type": "IDOR",
                "severity": "P1",
                "description": "Identical structure returned for Auth and Unauth requests.",
                "confidence": 90
            }
        return {"is_bug": False}
      
