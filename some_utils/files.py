import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def path_from_dir(dir_in: Path, extension: str | tuple[str]):
    for path in dir_in.iterdir():
        if not path.name.lower().endswith(extension):
            logger.info(f"unmanaged file: {path}")
            continue
        yield path
