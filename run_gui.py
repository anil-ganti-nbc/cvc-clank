"""Windows-friendly GUI launcher that resolves the local src tree directly."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from cvc.gui import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
