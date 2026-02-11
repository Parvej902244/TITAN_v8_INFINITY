import asyncio

class OrionAI:
    async def run_tool(self, cmd):
        try:
            proc = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            return stdout.decode().splitlines()
        except: return []

    async def discover(self, target):
        tasks = [
            self.run_tool(f"gau {target} --subs | head -n 50"),
            self.run_tool(f"katana -u {target} -d 2 -silent -nc")
        ]
        results = await asyncio.gather(*tasks)
        endpoints = set()
        for r in results:
            endpoints.update(r)
        return list(endpoints)
      
