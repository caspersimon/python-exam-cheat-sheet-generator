from pathlib import Path
import unittest

from scripts.check_file_lengths import find_violations


class FileLengthPolicyTests(unittest.TestCase):
    def test_no_code_file_exceeds_500_lines(self) -> None:
        root = Path(__file__).resolve().parents[1]
        violations = find_violations(root, max_lines=500)
        if violations:
            message = "\n".join(
                f"{violation.path.relative_to(root)}: {violation.line_count} lines"
                for violation in violations
            )
            self.fail(f"Code file length policy violations detected:\n{message}")


if __name__ == "__main__":
    unittest.main()
