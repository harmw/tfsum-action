import unittest


class Noop(unittest.TestCase):

    def setUp(self) -> None:
        """ none """

    def tearDown(self) -> None:
        """ none """

    def test_sadness(self) -> None:
        self.assertEqual(42, 42)


if __name__ == '__main__':
    unittest.main()
