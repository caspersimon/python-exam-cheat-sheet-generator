from pathlib import Path
import subprocess
import unittest


class JavaScriptSyntaxTests(unittest.TestCase):
    def test_app_scripts_parse(self) -> None:
        root = Path(__file__).resolve().parents[1]
        app_dir = root / "app"
        js_files = sorted(app_dir.glob("*.js"))
        self.assertTrue(js_files, "No JS files found under app/")

        for js_file in js_files:
            with self.subTest(file=js_file.name):
                result = subprocess.run(["node", "--check", str(js_file)], capture_output=True, text=True)
                self.assertEqual(
                    result.returncode,
                    0,
                    f"node --check failed for {js_file.name}: {result.stderr.strip()}",
                )


if __name__ == "__main__":
    unittest.main()
