# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client


# Create your tests here.
class UserViewTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_username_displayed(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'testuser')


class CreateTourViewTests(TestCase):
    def test_page_loads(self):
        response = self.client.get(reverse("create_tours"))
        self.assertEqual(response.status_code, 200)

    def test_google_maps_connects(self):
        response = self.client.get(reverse("create_tours"))
        self.assertContains(response, 'maps.googleapis.com/maps/api/js?key=')

    def test_add_to_tour_works(self):  # if we change form names this test will fail, we can fix this test later
        response = self.client.get(reverse("create_tours"))
        content = response.content.decode('utf-8')
        clemons_library_count = content.count('Clemons Library')
        uva_bookstore_count = content.count('UVA Bookstore')
        scott_stadium_count = content.count('Scott Stadium')

        form_data = {
            'clem': True,
            'bookstore': True,
        }

        response = self.client.post(reverse('create_tours'), data=form_data)
        content = response.content.decode('utf-8')

        clemons_library_count_final = content.count('Clemons Library')
        uva_bookstore_count_final = content.count('UVA Bookstore')
        scott_stadium_count_final = content.count('Scott Stadium')

        self.assertEqual(clemons_library_count, clemons_library_count_final)
        self.assertEqual(uva_bookstore_count, uva_bookstore_count_final)
        self.assertEqual(scott_stadium_count, scott_stadium_count_final)


class DiscoveryViewTests(TestCase):
    def test_page_loads(self):
        response = self.client.get(reverse("discovery"))
        self.assertEqual(response.status_code, 200)


class ThanKYouViewTests(TestCase):
    def test_page_loads(self):
        response = self.client.get(reverse("thank_you"))
        self.assertEqual(response.status_code, 200)


class Dashboard(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_dashboard_page_loads(self):
        self.client.login(username='testuser', password='testpassword')
        dashboard_url = reverse("dashboard")
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)

    def test_return_to_home_button(self):
        self.client.login(username='testuser', password='testpassword')
        dashboard_url = reverse("dashboard")
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)
        home_url = reverse("home")
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to UVA Tours!')

