import os
from pathlib import Path
from typing import Optional, Any, Dict
import yaml
from pydantic import BaseModel, Field

class ServerConfig(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080)
    transport: str = Field(default="streamable-http")

class DeviceConfig(BaseModel):
    default_timeout: float = Field(default=10.0)
    poll_interval: float = Field(default=1.0)

class LoggingConfig(BaseModel):
    level: str = Field(default="INFO")
    file_path: str = Field(default="logs/taskgenie.log")
    stdout_suppress: bool = Field(default=True)

class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    device: DeviceConfig = Field(default_factory=DeviceConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Load configuration from a YAML file.
    
    Tries the following locations in order:
    1. The explicitly provided config_path
    2. config/default_config.yaml relative to current working directory
    3. config/default_config.yaml relative to this source file
    
    If no file is found, returns default settings.
    """
    resolved_path: Optional[Path] = None
    
    if config_path:
        resolved_path = Path(config_path)
    else:
        # Check current working directory
        cwd_path = Path("config/default_config.yaml")
        if cwd_path.exists():
            resolved_path = cwd_path
        else:
            # Fallback to source tree lookup
            source_root = Path(__file__).resolve().parents[3]
            source_path = source_root / "config" / "default_config.yaml"
            if source_path.exists():
                resolved_path = source_path
                
    if resolved_path and resolved_path.exists():
        try:
            with open(resolved_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                # Handle environment overrides if necessary
                return AppConfig.model_validate(data)
        except Exception as e:
            # Fall back to defaults if parsing fails
            print(f"Warning: Failed to load config from {resolved_path} due to: {e}. Using defaults.")
            
    return AppConfig()
