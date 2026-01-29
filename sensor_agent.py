import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from datetime import datetime
from disaster_environment import DisasterEnvironment
import json

class SensorAgent(Agent):
    
    def __init__(self, jid, password, environment):
        super().__init__(jid, password)
        self.environment = environment
        self.event_log = []
    
    class PerceptionBehaviour(PeriodicBehaviour):
        
        async def run(self):
            """Monitor environment every period"""
            # Simulate a disaster event
            zone, disaster_type, severity = self.agent.environment.simulate_disaster()
            
            percept = {
                "timestamp": str(datetime.now()),
                "zone": zone,
                "disaster_type": disaster_type,
                "severity": severity,
                "status": "CRITICAL" if severity > 7 else "MODERATE" if severity > 4 else "MINOR"
            }
            
            # Log the event
            self.agent.event_log.append(percept)
            
            # Print perception
            print(f"[{percept['timestamp']}] DETECTED: {disaster_type.upper()} in {zone} - Severity: {severity}/10 ({percept['status']})")
            
            # Save to file
            self.save_log()
        
        def save_log(self):
            """Save event log to file"""
            with open("event_logs.json", "w") as f:
                json.dump(self.agent.event_log, f, indent=2)
    
    async def setup(self):
        print(f"SensorAgent {self.jid} is online and monitoring...")
        
        # Add periodic behaviour - monitors every 3 seconds
        behaviour = self.PerceptionBehaviour(period=3)
        self.add_behaviour(behaviour)


async def main():
    # Create disaster environment
    environment = DisasterEnvironment()
    
    # Create sensor agent
    sensor = SensorAgent("sensor@localhost", "password", environment)
    await sensor.start()
    
    print("SensorAgent started. Monitoring environment every 3 seconds...")
    print("Press Ctrl+C to stop.\n")
    
    await spade.wait_until_finished(sensor)

if __name__ == "__main__":
    spade.run(main())