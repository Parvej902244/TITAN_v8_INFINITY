import asyncio
import sys
import yaml
import logging
from core.http_engine import AsyncHttpEngine
from core.storage import StorageEngine
from core.system_monitor import SystemMonitor
from core.negative_memory import NegativeMemory
from core.state_graph import StateGraphEngine
from core.defense_monitor import DefenseMonitor
from core.evidence import EvidenceChain
from core.intelligence_memory import IntelligenceMemory
from core.global_memory import GlobalExperienceMemory

from ai.atlas import AtlasAI
from ai.orion import OrionAI
from ai.logos import LogosAI
from ai.riskos import RiskOS
from ai.criticus import CriticusAI
from ai.spectrum import SpectrumAI
from ai.scribe import ScribeAI
from ai.semantics import SemanticAI
from ai.correlation import CorrelationAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main(target_url):
    print(f"🌌 TITAN_v8∞∞ LAUNCHING ON TARGET: {target_url}")
    
    with open("config/defaults.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Initialize Core
    storage = StorageEngine(target_url)
    http = AsyncHttpEngine(config)
    monitor = SystemMonitor(config)
    neg_mem = NegativeMemory()
    state_graph = StateGraphEngine()
    defense = DefenseMonitor()
    int_mem = IntelligenceMemory()
    glob_mem = GlobalExperienceMemory()
    
    # Initialize AI
    atlas = AtlasAI(config, neg_mem)
    orion = OrionAI()
    logos = LogosAI()
    riskos = RiskOS()
    criticus = CriticusAI()
    spectrum = SpectrumAI()
    scribe = ScribeAI()
    semantics = SemanticAI()
    correlation = CorrelationAI()

    # Load State
    prev = storage.load_state()
    atlas.load_state(prev)

    await http.start()

    try:
        while True:
            # Health & Defense Checks
            if not await monitor.check_health() or defense.should_slow_down():
                logging.warning("⚠️ Resource/Defense Throttling...")
                await asyncio.sleep(5)
                continue

            # Context for Planning
            context = {
                "new_endpoints": len(spectrum.discovered) - len(spectrum.analyzed),
                "new_bugs": 0 # Logic to track this in real flow
            }
            
            action = atlas.plan_next_step(context)
            
            if "FINALIZE" in action:
                logging.info("🏁 Scan Complete.")
                break

            logging.info(f"🧠 Atlas: {action}")

            if "ORION" in str(action):
                eps = await orion.discover(target_url)
                spectrum.add_discovered(eps)
                for ep in eps:
                    if not int_mem.is_analyzed(ep):
                        atlas.queue.append(f"ANALYZE:{ep}")

            elif "ANALYZE" in str(action):
                target_ep = f"{target_url}/api/v1/user" # Mock, would parse from action string
                
                if not neg_mem.is_known_safe("GET", target_ep):
                    ev = EvidenceChain()
                    ev.add_evidence("Discovery", "Found via Orion", 10)
                    
                    r_high = await http.request("GET", target_ep, context="user_high")
                    defense.record_response(r_high['status'], r_high['length'])
                    
                    r_low = await http.request("GET", target_ep, context="anon")
                    
                    # Semantics Check
                    params = {"user_id": 123} # Mock
                    p_types = semantics.classify(params)
                    correlation.ingest(target_ep, params)
                    
                    # Logic Analysis
                    res = logos.analyze_idor(r_high, r_low)
                    if res['is_bug']:
                        ev.add_evidence("Logic", "IDOR Detected", 80)
                        res['evidence_explanation'] = ev.get_explanation()
                        
                        final_bug = riskos.evaluate(res)
                        if criticus.validate(final_bug):
                            final_bug = scribe.format(final_bug)
                            storage.save_bug(final_bug)
                            glob_mem.learn_vuln_param("user_id") # Learn
                    else:
                        neg_mem.mark_safe("GET", target_ep)
                    
                    int_mem.mark_analyzed(target_ep)
                    spectrum.add_analyzed(target_ep)

            await asyncio.sleep(0.5)

    except KeyboardInterrupt:
        logging.info("🛑 Saving state...")
    finally:
        storage.save_state(atlas.get_state())
        await http.stop()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./titan scan https://target.com")
        sys.exit(1)
    asyncio.run(main(sys.argv[2]))
              
