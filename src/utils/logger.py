"""Logging utilities."""

from __future__ import annotations

import logging
from pathlib import Path

from config import LOGS_DIR


def configure_logger(name: str) -> logging.Logger:
    """Create a logger configured for file and stream output."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(LOGS_DIR / "application.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
