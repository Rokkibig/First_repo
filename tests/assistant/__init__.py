"""Assistant test suite."""

from __future__ import annotations

import importlib
import sys

if "assistant" not in sys.modules:
    sys.modules["assistant"] = importlib.import_module("assistant")
