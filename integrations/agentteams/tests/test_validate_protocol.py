import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_protocol.py"
SPEC = importlib.util.spec_from_file_location("validate_protocol", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ProtocolValidationTests(unittest.TestCase):
    def test_bundled_protocol_is_valid(self):
        self.assertEqual(MODULE.main(), 0)

    def test_rejects_missing_committee_role(self):
        role_map = MODULE.load_json("role-map.json")
        role_map["roles"] = [role for role in role_map["roles"] if role["id"] != "thesis_bear"]
        with self.assertRaises(ValueError):
            MODULE.validate_role_map(role_map)


if __name__ == "__main__":
    unittest.main()
