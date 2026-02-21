import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from datetime import datetime
from disaster_environment import DisasterEnvironment
from rescue_agent import RescueAgent
import json

class SensorAgent(Agent):
    
    def __init__(self, jid, password, environment, rescue_jid):
        super().__init__(jid, password)
        self.environment = environment
        self.rescue_jid = rescue_jid
        self.event_log = []
    
    class PerceptionBehaviour(PeriodicBehaviour):
        
        async def run(self):
            # Simulate disaster
            zone, disaster_type, severity = self.agent.environment.simulate_disaster()
            
            percept = {
                "timestamp": str(datetime.now()),
                "zone": zone,
                "disaster_type": disaster_type,
                "severity": severity,
                "status": "CRITICAL" if severity > 7 else "MODERATE" if severity > 4 else "MINOR"
            }
            
            self.agent.event_log.append(percept)
            print(f"[SENSOR] Detected: {disaster_type.upper()} in {zone} - Severity: {severity}/10")
            
            # Send message to RescueAgent
            msg = Message(to=self.agent.rescue_jid)
            msg.body = json.dumps(percept)
            msg.set_metadata("performative", "inform")
            await self.send(msg)
            print(f"[SENSOR] Alert sent to RescueAgent\n")
    
    async def setup(self):
        print(f"SensorAgent {self.jid} monitoring...\n")
        behaviour = self.PerceptionBehaviour(period=5)
        self.add_behaviour(behaviour)


async def main():
    environment = DisasterEnvironment()
    
    # Start both agents
    rescue = RescueAgent("rescue@localhost", "password")
    sensor = SensorAgent("sensor@localhost", "password", environment, "rescue@localhost")
    
    await rescue.start()
    await sensor.start()
    
    print("=== Disaster Response System Active ===")
    print("SensorAgent detecting disasters every 5 seconds")
    print("RescueAgent responding based on FSM")
    print("Press Ctrl+C to stop\n")
    
    await spade.wait_until_finished(rescue)

if __name__ == "__main__":
    spade.run(main())