"""Write validation output without replacing archived inputs."""

import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ENV = 'QCH_VALIDATION_OUTPUT_DIR'


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf-8', dir=path.parent, prefix=f'.{path.name}.', delete=False,
    ) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
            stream.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def write_result(path, content):
    """Preserve a script's direct output path unless a run directory was selected."""
    directory = os.environ.get(OUTPUT_ENV)
    if directory:
        if path.is_relative_to(ROOT / 'work/research'):
            path = Path(directory) / path.relative_to(ROOT / 'work/research')
        else:
            # Include the experiment group so names from different checks stay distinct.
            path = Path(directory) / path.relative_to(ROOT / 'codes')
    write_atomic(path, content)
