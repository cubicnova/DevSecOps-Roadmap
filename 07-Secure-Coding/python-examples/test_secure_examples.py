"""Regression tests for the educational secure-coding examples."""
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def load_example(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, EXAMPLES / filename)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SecureCodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validation = load_example("01-input-validation.py", "input_validation")
        cls.sql = load_example("02-sql-injection.py", "sql_example")
        cls.passwords = load_example("03-password-security.py", "password_security")
        cls.secrets = load_example("04-secrets-management.py", "secrets_example")
        cls.paths = load_example("05-path-traversal.py", "path_security")
        cls.commands = load_example("06-command-injection.py", "command_security")
        cls.json_example = load_example("07-unsafe-deserialization.py", "safe_json")
        cls.logging = load_example("09-secure-logging.py", "secure_logging")

    def test_valid_username(self):
        self.assertEqual(self.validation.validate_username("alice_01"), "alice_01")

    def test_invalid_username_rejected(self):
        for candidate in ("../secret", "user name", "", "ab", "x" * 21):
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    self.validation.validate_username(candidate)

    def test_sql_looking_input_is_data(self):
        connection = sqlite3.connect(":memory:")
        try:
            connection.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL)"
            )
            connection.execute("INSERT INTO users (username) VALUES (?)", ("alice",))
            self.assertIsNone(self.sql.find_user(connection, "' OR '1'='1"))
            self.assertEqual(self.sql.find_user(connection, "alice")[1], "alice")
        finally:
            connection.close()

    def test_password_verification(self):
        salt, digest = self.passwords.hash_password("Strong-Test-123!")
        self.assertTrue(self.passwords.verify_password("Strong-Test-123!", salt, digest))
        self.assertFalse(self.passwords.verify_password("wrong", salt, digest))
        salt2, digest2 = self.passwords.hash_password("Strong-Test-123!")
        self.assertNotEqual(salt, salt2)
        self.assertNotEqual(digest, digest2)

    def test_empty_password_rejected(self):
        with self.assertRaises(ValueError):
            self.passwords.hash_password("")

    def test_missing_secret_rejected(self):
        import os
        old = os.environ.pop("DEMO_API_KEY", None)
        try:
            with self.assertRaises(RuntimeError):
                self.secrets.get_api_key()
        finally:
            if old is not None:
                os.environ["DEMO_API_KEY"] = old

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "allowed"
            root.mkdir()
            (parent / "secret.txt").write_text("secret", encoding="utf-8")
            (root / "welcome.txt").write_text("hello", encoding="utf-8")
            self.assertEqual(self.paths.read_allowed_file(root, "welcome.txt"), "hello")
            with self.assertRaises(ValueError):
                self.paths.read_allowed_file(root, "../secret.txt")

    def test_command_action_allowlist(self):
        with self.assertRaises(ValueError):
            self.commands.run_action("status; echo unsafe")

    def test_json_profile_accepts_expected_shape(self):
        result = self.json_example.parse_profile(
            '{"username":"alice","display_name":"Alice"}'
        )
        self.assertEqual(result["username"], "alice")

    def test_json_profile_rejects_extra_fields(self):
        with self.assertRaises(ValueError):
            self.json_example.parse_profile(
                '{"username":"alice","display_name":"Alice","is_admin":true}'
            )

    def test_json_profile_rejects_wrong_type(self):
        with self.assertRaises(ValueError):
            self.json_example.parse_profile(
                '{"username":123,"display_name":"Alice"}'
            )

    def test_log_redaction(self):
        result = self.logging.redact_sensitive_data(
            "token=example-secret password=example-password"
        )
        self.assertNotIn("example-secret", result)
        self.assertNotIn("example-password", result)
        self.assertIn("[REDACTED]", result)


if __name__ == "__main__":
    unittest.main()
