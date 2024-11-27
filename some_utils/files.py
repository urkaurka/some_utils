import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def paths_from_dir(dir_in: Path, extension: str | tuple[str]):
    for path in dir_in.glob("**/*"):
        if path.is_dir():
            continue
        if not path.name.lower().endswith(extension) and not path.is_dir():
            logger.info(f"unmanaged file: {path}")
            continue
        yield path


def is_dir_empty(_dir: Path) -> bool:
    assert _dir.is_dir()
    return not any(_dir.iterdir())
