import random
from datetime import datetime

class DisasterEnvironment:
    def __init__(self):
        self.zones = {
            "Zone_A": {"severity": 0, "type": None},
            "Zone_B": {"severity": 0, "type": None},
            "Zone_C": {"severity": 0, "type": None},
            "Zone_D": {"severity": 0, "type": None}
        }
    
    def simulate_disaster(self):
        """Randomly trigger disasters in zones"""
        zone = random.choice(list(self.zones.keys()))
        disaster_type = random.choice(["flood", "fire", "earthquake"])
        severity = random.randint(1, 10)  # 1=minor, 10=critical
        
        self.zones[zone] = {
            "severity": severity,
            "type": disaster_type
        }
        
        return zone, disaster_type, severity
    
    def get_zone_status(self, zone):
        """Get current status of a zone"""
        return self.zones.get(zone)
    
    def get_all_zones(self):
        """Get status of all zones"""
        return self.zones