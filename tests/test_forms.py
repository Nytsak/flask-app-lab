import unittest
from app import app
from app.users.forms import ContactForm, LoginForm


class TestContactForm(unittest.TestCase):
    """Тести для ContactForm"""

    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Очищення після кожного тесту"""
        self.ctx.pop()

    def test_contact_form_creation(self):
        """Тест створення ContactForm"""
        form = ContactForm()
        self.assertIsNotNone(form)
        self.assertIn('name', form._fields)
        self.assertIn('email', form._fields)
        self.assertIn('phone', form._fields)
        self.assertIn('subject', form._fields)
        self.assertIn('message', form._fields)
        self.assertIn('submit', form._fields)

    def test_contact_form_name_validators(self):
        """Тест валідаторів поля name"""
        form = ContactForm()
        validators = [v.__class__.__name__ for v in form.name.validators]
        self.assertIn('DataRequired', validators)
        self.assertIn('Length', validators)

    def test_contact_form_email_validators(self):
        """Тест валідаторів поля email"""
        form = ContactForm()
        validators = [v.__class__.__name__ for v in form.email.validators]
        self.assertIn('DataRequired', validators)
        self.assertIn('Email', validators)

    def test_contact_form_phone_validators(self):
        """Тест валідаторів поля phone"""
        form = ContactForm()
        validators = [v.__class__.__name__ for v in form.phone.validators]
        self.assertIn('DataRequired', validators)
        self.assertIn('Regexp', validators)

    def test_contact_form_subject_validators(self):
        """Тест валідаторів поля subject"""
        form = ContactForm()
        validators = [v.__class__.__name__ for v in form.subject.validators]
        self.assertIn('DataRequired', validators)

    def test_contact_form_message_validators(self):
        """Тест валідаторів поля message"""
        form = ContactForm()
        validators = [v.__class__.__name__ for v in form.message.validators]
        self.assertIn('DataRequired', validators)
        self.assertIn('Length', validators)

    def test_contact_form_valid_data(self):
        """Тест валідації з коректними даними"""
        form = ContactForm(
            name='Олег',
            email='oleg@test.com',
            phone='380123456789',
            subject='general',
            message='Тестове повідомлення'
        )
        self.assertTrue(len(form.name.data) >= 4)
        self.assertTrue(len(form.name.data) <= 10)

    def test_contact_form_invalid_name_too_short(self):
        """Тест валідації з занадто коротким ім'ям"""
        form = ContactForm(
            name='Jon',
            email='test@test.com',
            phone='380123456789',
            subject='general',
            message='Test message'
        )
        self.assertFalse(form.validate())
        self.assertIn('name', form.errors)

    def test_contact_form_invalid_email(self):
        """Тест валідації з невірним email"""
        form = ContactForm(
            name='TestUser',
            email='invalid-email',
            phone='380123456789',
            subject='general',
            message='Test message'
        )
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)

    def test_contact_form_invalid_phone(self):
        """Тест валідації з невірним телефоном"""
        form = ContactForm(
            name='TestUser',
            email='test@test.com',
            phone='123456',
            subject='general',
            message='Test message'
        )
        self.assertFalse(form.validate())
        self.assertIn('phone', form.errors)


class TestLoginForm(unittest.TestCase):
    """Тести для LoginForm"""

    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Очищення після кожного тесту"""
        self.ctx.pop()

    def test_login_form_creation(self):
        """Тест створення LoginForm"""
        form = LoginForm()
        self.assertIsNotNone(form)
        self.assertIn('username', form._fields)
        self.assertIn('password', form._fields)
        self.assertIn('remember', form._fields)
        self.assertIn('submit', form._fields)

    def test_login_form_username_validators(self):
        """Тест валідаторів поля username"""
        form = LoginForm()
        validators = [v.__class__.__name__ for v in form.username.validators]
        self.assertIn('DataRequired', validators)

    def test_login_form_password_validators(self):
        """Тест валідаторів поля password"""
        form = LoginForm()
        validators = [v.__class__.__name__ for v in form.password.validators]
        self.assertIn('DataRequired', validators)
        self.assertIn('Length', validators)

    def test_login_form_remember_field(self):
        """Тест наявності поля remember (BooleanField)"""
        form = LoginForm()
        self.assertIn('remember', form._fields)
        self.assertEqual(form.remember.type, 'BooleanField')

    def test_login_form_valid_data(self):
        """Тест валідації з коректними даними"""
        form = LoginForm(
            username='admin',
            password='admin123',
            remember=True
        )
        self.assertTrue(len(form.password.data) >= 4)
        self.assertTrue(len(form.password.data) <= 10)

    def test_login_form_invalid_password_too_short(self):
        """Тест валідації з занадто коротким паролем"""
        form = LoginForm(
            username='admin',
            password='123',
            remember=False
        )
        self.assertFalse(form.validate())
        self.assertIn('password', form.errors)

    def test_login_form_invalid_password_too_long(self):
        """Тест валідації з занадто довгим паролем"""
        form = LoginForm(
            username='admin',
            password='12345678901',
            remember=False
        )
        self.assertFalse(form.validate())
        self.assertIn('password', form.errors)

    def test_login_form_empty_fields(self):
        """Тест валідації з порожніми полями"""
        form = LoginForm(
            username='',
            password=''
        )
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
