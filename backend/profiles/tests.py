from io import BytesIO
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from profiles.models import Profile


User = get_user_model()


def get_test_image_file(name='test_image', ext='JPEG', size=(100, 100), color=(255, 0, 0)):
    image_io = BytesIO()
    image = Image.new('RGB', size, color)
    image.save(image_io, ext)
    image_io.seek(0)

    return SimpleUploadedFile(name, image_io.read(), content_type='image/jpeg')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com',
        )

    def tearDown(self):
        profile = self.get_profile()
        if profile.image:
            profile.image.delete(save=False)

    def get_profile(self):
        return self.user.profile

    def test_profile_created(self):
        profile = self.get_profile()

        self.assertTrue(User.objects.first().profile)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.display_name, profile.user.username)

    def test_image_upload(self):
        image = get_test_image_file()
        profile = self.get_profile()

        profile.image = image
        profile.save()

        self.assertTrue(profile.image)
        self.assertTrue(profile.image.name.endswith('jpg'))

    def test_image_compression(self):
        image = get_test_image_file()
        profile = self.get_profile()

        profile.image = image
        profile.save()

        self.assertLess(profile.image.size, image.size)

    def test_image_url_returns_default(self):
        profile = self.get_profile()

        self.assertIn('defaults/default.png', profile.image_url)
        