"""Read external application configuration."""
import json
from pathlib import Path


def load_config(config_path):
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)
    required = ("storage_format", "data_file", "log_file")
    missing = [key for key in required if key not in config]
    if missing:
        raise ValueError("Missing configuration key(s): " + ", ".join(missing))
    return config
