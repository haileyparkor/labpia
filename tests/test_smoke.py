import os
import tempfile
import unittest

TEMP_DIR = tempfile.TemporaryDirectory()
os.environ["LABPIA_DB"] = os.path.join(TEMP_DIR.name, "test.db")

import app as app_module  # noqa: E402
import db  # noqa: E402


class SmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.init_db()

    @classmethod
    def tearDownClass(cls):
        TEMP_DIR.cleanup()

    def setUp(self):
        self.client = app_module.app.test_client()

    def test_pages(self):
        for path in ["/", "/search", "/location", "/admin/reagents/import", "/scan"]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_missing_supply(self):
        self.assertEqual(self.client.get("/supply/999999").status_code, 404)


if __name__ == "__main__":
    unittest.main()
