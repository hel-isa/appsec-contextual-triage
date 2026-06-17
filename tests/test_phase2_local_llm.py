import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "phase2-local-llm" / "appsec_llm_triage.py"


def load_module():
    if not MODULE_PATH.exists():
        raise FileNotFoundError(f"Missing module under test: {MODULE_PATH}")

    spec = importlib.util.spec_from_file_location("appsec_llm_triage", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module spec for: {MODULE_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalVerdictTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_get_local_verdict_blocks_when_read_pickle_is_present(self):
        source_code = "import pandas as pd\npd.read_pickle('payload.pkl')"

        verdict = self.module.get_local_verdict(source_code)

        self.assertEqual(verdict, "BLOCK")

    def test_get_local_verdict_allows_when_read_pickle_is_absent(self):
        source_code = "import pandas as pd\npd.read_csv('safe.csv')"

        verdict = self.module.get_local_verdict(source_code)

        self.assertEqual(verdict, "ALLOW")


if __name__ == "__main__":
    unittest.main()