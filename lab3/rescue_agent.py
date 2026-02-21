import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime
import json
import asyncio

class RescueAgent(Agent):
    
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.state = "IDLE"
        self.current_task = None
        self.execution_trace = []
        self.goal = "Maximize lives saved"
        
    class ReactiveRescueBehaviour(CyclicBehaviour):
        
        async def run(self):
            # Wait for messages from SensorAgent
            msg = await self.receive(timeout=10)
            
            if msg:
                # Parse the disaster event
                event = json.loads(msg.body)
                await self.handle_event(event)
            else:
                # No message, maintain current state
                await self.idle_check()
        
        async def handle_event(self, event):
            """React to disaster events based on FSM"""
            timestamp = str(datetime.now())
            
            # STATE: IDLE → Check if we should respond
            if self.agent.state == "IDLE":
                if event['severity'] > 4:
                    # Transition to RESPONDING
                    self.agent.state = "RESPONDING"
                    self.agent.current_task = event
                    
                    trace = {
                        "timestamp": timestamp,
                        "event": "disaster_detected",
                        "data": event,
                        "state_transition": "IDLE → RESPONDING",
                        "reason": f"Severity {event['severity']} requires response"
                    }
                    self.agent.execution_trace.append(trace)
                    print(f"[{timestamp}] STATE CHANGE: IDLE → RESPONDING")
                    print(f"   Task: Respond to {event['disaster_type']} in {event['zone']}")
                    
                    # Simulate traveling to location
                    await asyncio.sleep(2)
                    await self.arrive_at_location()
                else:
                    print(f"[{timestamp}] Event ignored: Severity {event['severity']} too low (threshold: 5)")
            
            elif self.agent.state == "RESPONDING":
                # Already responding, queue or ignore
                print(f"[{timestamp}] Already responding to a task. Event queued.")
        
        async def arrive_at_location(self):
            """Transition: RESPONDING → RESCUING"""
            timestamp = str(datetime.now())
            self.agent.state = "RESCUING"
            
            trace = {
                "timestamp": timestamp,
                "event": "arrived_at_location",
                "state_transition": "RESPONDING → RESCUING",
                "location": self.agent.current_task['zone']
            }
            self.agent.execution_trace.append(trace)
            print(f"[{timestamp}] STATE CHANGE: RESPONDING → RESCUING")
            print(f"   Location: {self.agent.current_task['zone']}")
            
            # Simulate rescue operation
            await asyncio.sleep(3)
            await self.complete_rescue()
        
        async def complete_rescue(self):
            """Transition: RESCUING → RETURNING"""
            timestamp = str(datetime.now())
            self.agent.state = "RETURNING"
            
            trace = {
                "timestamp": timestamp,
                "event": "rescue_completed",
                "state_transition": "RESCUING → RETURNING",
                "task": self.agent.current_task
            }
            self.agent.execution_trace.append(trace)
            print(f"[{timestamp}] STATE CHANGE: RESCUING → RETURNING")
            print(f"   Rescue completed at {self.agent.current_task['zone']}")
            
            # Simulate returning to base
            await asyncio.sleep(2)
            await self.return_to_base()
        
        async def return_to_base(self):
            """Transition: RETURNING → IDLE"""
            timestamp = str(datetime.now())
            self.agent.state = "IDLE"
            
            trace = {
                "timestamp": timestamp,
                "event": "returned_to_base",
                "state_transition": "RETURNING → IDLE",
                "ready_for_next_task": True
            }
            self.agent.execution_trace.append(trace)
            print(f"[{timestamp}] STATE CHANGE: RETURNING → IDLE")
            print(f"   Ready for next assignment\n")
            
            self.agent.current_task = None
            self.save_trace()
        
        async def idle_check(self):
            """Periodic check when idle"""
            if self.agent.state == "IDLE":
                pass  # Just waiting
        
        def save_trace(self):
            """Save execution trace to file"""
            with open("execution_trace.json", "w") as f:
                json.dump(self.agent.execution_trace, f, indent=2)
    
    async def setup(self):
        print(f"RescueAgent {self.jid} online")
        print(f"Goal: {self.goal}")
        print(f"Initial State: {self.state}\n")
        
        behaviour = self.ReactiveRescueBehaviour()
        self.add_behaviour(behaviour)