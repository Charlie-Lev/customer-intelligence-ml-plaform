"""Logging utilities."""

from __future__ import annotations

import logging


_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(
    name: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """Return a configured console logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(handler)

    return logger
