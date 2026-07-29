from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import InviteCode

User = get_user_model()

class InviteCodeTests(APITestCase):
    def setUp(self):
        # Clear cache before each test
        cache.clear()
        
        # Create an admin user
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='Password123!',
            role='admin',
            is_active=True
        )
        # Create a regular user
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='Password123!',
            role='user',
            is_active=True
        )

    def test_admin_can_create_invite_code(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('invite-code')
        
        # Test creating with custom code
        response = self.client.post(url, {'code': 'TESTCODE123'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 'TESTCODE123')
        self.assertFalse(response.data['is_used'])
        
        # Test creating with auto-generated code
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['code'])
        self.assertEqual(len(response.data['code']), 8)

    def test_regular_user_cannot_create_invite_code(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('invite-code')
        response = self.client.post(url, {'code': 'TESTCODE123'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_invite_codes(self):
        InviteCode.objects.create(code='CODE1')
        InviteCode.objects.create(code='CODE2')
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('invite-code')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_regular_user_cannot_list_invite_codes(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('invite-code')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registration_flow_with_invite_code(self):
        # Create a valid unused invite code
        invite = InviteCode.objects.create(code='WELCOME2026')
        
        url_register = reverse('register')
        
        # 1. Register with missing invite code
        response = self.client.post(url_register, {
            'email': 'newuser@example.com',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('invite_code', response.data)

        # 2. Register with invalid invite code
        response = self.client.post(url_register, {
            'email': 'newuser@example.com',
            'password': 'Password123!',
            'invite_code': 'INVALIDCODE'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. Register with valid invite code (should succeed and generate OTP in cache)
        response = self.client.post(url_register, {
            'email': 'newuser@example.com',
            'password': 'Password123!',
            'invite_code': 'WELCOME2026'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that invite is NOT marked as used yet
        invite.refresh_from_db()
        self.assertFalse(invite.is_used)

        # Get the OTP from cache to verify
        cache_key = 'registration_otp_newuser@example.com'
        cached_data = cache.get(cache_key)
        self.assertIsNotNone(cached_data)
        otp = cached_data['otp']

        # 4. Verify OTP (should create user, mark invite code as used)
        url_verify = reverse('verify-otp')
        response = self.client.post(url_verify, {
            'email': 'newuser@example.com',
            'otp': otp,
            'purpose': 'registration'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Invite code should now be marked as used and linked to the new user
        invite.refresh_from_db()
        self.assertTrue(invite.is_used)
        self.assertEqual(invite.used_by.email, 'newuser@example.com')
        self.assertIsNotNone(invite.used_at)

        # 5. Try to register another user with the same used invite code (should fail)
        response = self.client.post(url_register, {
            'email': 'anotheruser@example.com',
            'password': 'Password123!',
            'invite_code': 'WELCOME2026'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

