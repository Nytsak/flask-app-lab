import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list_page(self):
        """Тест маршруту /products/ - список продуктів."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Smartphone", response.data)
        self.assertIn(b"Headphones", response.data)
        self.assertIn(b"25000", response.data)

    def test_product_detail_page(self):
        """Тест маршруту /products/<id> - деталі продукту."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"25000", response.data)
        self.assertIn(b"Powerful laptop for work and study", response.data)


if __name__ == "__main__":
    unittest.main()
