import unittest
from collect import get_access_token

class TestCollect(unittest.TestCase):
    def test_access_token(self):
        try:
            token = get_access_token()
            self.assertIsNotNone(token, "Le token n'a pas été généré correctement")
        except Exception as e:
            self.fail(f"Le test a échoué avec une exception : {str(e)}")

if __name__ == "__main__":
    unittest.main()

