"""Project path utilities."""

from __future__ import annotations

from pathlib import Path


def _discover_project_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__).resolve()).resolve()

    if current.is_file():
        current = current.parent

    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists():
            return candidate

    for candidate in [current, *current.parents]:
        if (candidate / "src").exists():
            return candidate

    raise RuntimeError("Could not determine the project root.")


PROJECT_ROOT = _discover_project_root()


def get_project_path(
    *parts: str | Path,
    create_parent: bool = False,
) -> Path:
    """Return an absolute path relative to the project root."""
    path = PROJECT_ROOT.joinpath(*map(Path, parts))

    if create_parent:
        path.parent.mkdir(parents=True, exist_ok=True)

    return path
