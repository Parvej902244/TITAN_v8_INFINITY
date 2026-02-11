from collections import deque
import time

class DefenseMonitor:
    def __init__(self):
        self.history = deque(maxlen=50) # Increased window
        self.last_block_time = 0

    def record_response(self, status, body_len):
        self.history.append((status, body_len, time.time()))

    def should_slow_down(self):
        recent = [s for s, l, t in self.history if time.time() - t < 60]
        blocks = [s for s in recent if s in [403, 429]]
        soft_blocks = [s for s, l, t in self.history if s == 200 and l < 50] # Soft block detection
        
        if len(blocks) > 5 or len(soft_blocks) > 10:
            return True
        return False
      
