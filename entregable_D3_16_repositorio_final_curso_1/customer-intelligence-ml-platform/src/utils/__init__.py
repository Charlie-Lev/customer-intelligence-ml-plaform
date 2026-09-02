"""Shared project utilities."""

from .logger import get_logger
from .paths import PROJECT_ROOT, get_project_path

__all__ = ["get_logger", "PROJECT_ROOT", "get_project_path"]
