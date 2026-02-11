import psutil
import asyncio
import logging

class SystemMonitor:
    def __init__(self, config):
        self.max_ram = config['system']['ram_threshold']
        self.max_cpu = config['system']['cpu_threshold']
        self.paused = False

    async def check_health(self):
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        if mem.percent > self.max_ram or cpu > self.max_cpu:
            self.paused = True
            await asyncio.sleep(5)
            return False
        self.paused = False
        return True
      
