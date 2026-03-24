from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.exam_builder_dataset import OUTPUT_PATH, write_payload


def main() -> int:
    output = write_payload()
    print(json.dumps({"output_path": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
