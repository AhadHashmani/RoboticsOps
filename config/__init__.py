"""
Configuration management for RoboticsOps.
Loads robot configs, warehouse layout, and settings.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manage application configuration."""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.robot_configs = self._load_robot_configs()
        self.warehouse_layout = self._load_warehouse_layout()
    
    def _load_robot_configs(self) -> Dict[str, Any]:
        """Load robot configurations."""
        try:
            config_file = self.config_dir / "robot_configs.yaml"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading robot configs: {e}")
        
        # Default configs
        return {
            "AGV-001": {"type": "picker", "max_speed": 1.5, "capacity": 50},
            "AGV-002": {"type": "picker", "max_speed": 1.5, "capacity": 50},
            "AGV-003": {"type": "transporter", "max_speed": 2.0, "capacity": 100},
            "AGV-004": {"type": "transporter", "max_speed": 2.0, "capacity": 100},
        }
    
    def _load_warehouse_layout(self) -> Dict[str, Any]:
        """Load warehouse layout."""
        try:
            layout_file = self.config_dir / "warehouse_layout.json"
            if layout_file.exists():
                with open(layout_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading warehouse layout: {e}")
        
        # Default layout
        return {
            "width": 100,
            "height": 50,
            "stations": [
                {"id": f"Station-{i}", "position": (i*8, 25)} for i in range(1, 13)
            ]
        }


# Global config instance
_config_manager = None

def get_config() -> ConfigManager:
    """Get global config manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
