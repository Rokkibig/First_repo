"""Configuration helpers for data connectors."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_json_config(path: str | Path) -> Dict[str, Any]:
    """Load a JSON configuration file.

    Parameters
    ----------
    path:
        The path to the configuration file.

    Returns
    -------
    Dict[str, Any]
        Parsed configuration data. Returns an empty dictionary if the file
        does not exist.
    """
    config_path = Path(path)
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)
