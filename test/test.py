import unittest

from jusho import Jusho


class TestJusho(unittest.TestCase):
    """
    test class of jusho
    """
    postman = Jusho()

    def testfrompostal(self):
        self.assertEqual(self.postman.from_postal_code('160-0021').hyphen_postal, '160-0021')
        self.assertEqual(self.postman.address_from_town('大阪府', '三島郡島本町', '青葉', 'kanji').hyphen_postal, '618-0015')


if __name__ == "__main__":
    unittest.main()
