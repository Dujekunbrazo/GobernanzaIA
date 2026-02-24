import runpy
from pathlib import Path


if __name__ == "__main__":
    # Compatibility wrapper: canonical script lives in scripts/ops/.
    target = Path(__file__).resolve().parent / "ops" / "bitacora_append.py"
    runpy.run_path(str(target), run_name="__main__")
