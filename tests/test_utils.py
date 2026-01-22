import unittest
from utils import normalizar_precio

class TestUtils(unittest.TestCase):
    def test_precio_valido(self):
        self.assertEqual(normalizar_precio("123.45"), 123.45)

    def test_precio_invalido(self):
        self.assertEqual(normalizar_precio("abc"), 0.0)

if __name__ == "__main__":
    unittest.main()
