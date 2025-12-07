"""
PURPOSE:
Centralized logging setup for the entire application. Creates a single logger
instance that can be imported anywhere in the codebase.

Single logger named "pomogator" used across all modules
Console output with timestamp, level, and message formatting
Default log level: INFO
Prevents duplicate handlers if imported multiple times
"""

import logging

logger = logging.getLogger("pomogator")
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)