from django.test import TestCase
from django.contrib.auth.models import User
from backend.apps.users.forms import CustomUserCreationForm

class UserFormTest(TestCase):
    def test_clean_email_duplicate(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'password456',
            'password2': 'password456',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['This email is already in use'])

    def test_clean_email_unique(self):
        form_data = {
            'username': 'newuser',
            'email': 'unique@example.com',
            'password1': 'password456',
            'password2': 'password456',
        }
        form = CustomUserCreationForm(data=form_data)
        # Note: UserCreationForm also validates passwords, etc.
        # But we want to see if clean_email is called and works.
        # It might still be invalid due to other reasons, but we check email error.
        if not form.is_valid():
            self.assertNotIn('email', form.errors)
