"""
Unit tests for the mapa application.

Run tests with: python manage.py test mapa
"""

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Dzielnica, ZdarzenieSpoleczne, Komentarz


class DzielnicaModelTest(TestCase):
    """Tests for the Dzielnica model."""

    def setUp(self):
        """Set up test data."""
        self.dzielnica = Dzielnica.objects.create(
            dzielnica="Test District",
            geometry={"type": "Polygon", "coordinates": []},
            powierzchnia=10.5,
            kobiety_mlodzi=100,
            kobiety_dorosli=200,
            kobiety_seniorzy=50,
            mezczyzni_mlodzi=110,
            mezczyzni_dorosli=190,
            mezczyzni_seniorzy=45,
        )

    def test_dzielnica_creation(self):
        """Test that a Dzielnica can be created."""
        self.assertEqual(self.dzielnica.dzielnica, "Test District")
        self.assertEqual(self.dzielnica.powierzchnia, 10.5)

    def test_liczba_kobiet_property(self):
        """Test the liczba_kobiet computed property."""
        expected = 100 + 200 + 50
        self.assertEqual(self.dzielnica.liczba_kobiet, expected)

    def test_liczba_mezczyzn_property(self):
        """Test the liczba_mezczyzn computed property."""
        expected = 110 + 190 + 45
        self.assertEqual(self.dzielnica.liczba_mezczyzn, expected)

    def test_liczba_mieszkancow_property(self):
        """Test the total population computed property."""
        expected = (100 + 200 + 50) + (110 + 190 + 45)
        self.assertEqual(self.dzielnica.liczba_mieszkancow, expected)

    def test_to_geojson_feature(self):
        """Test GeoJSON feature generation."""
        feature = self.dzielnica.to_geojson_feature()
        self.assertEqual(feature["type"], "Feature")
        self.assertEqual(feature["properties"]["nazwa"], "Test District")
        self.assertIn("geometry", feature)


class ZdarzenieSpoleczneModelTest(TestCase):
    """Tests for the ZdarzenieSpoleczne model."""

    def setUp(self):
        """Set up test data."""
        self.zdarzenie = ZdarzenieSpoleczne.objects.create(
            lokalizacja_lat=54.35,
            lokalizacja_lng=18.65,
            kategoria2="zgloszenie",
            kategoria3="wypadek_drogowy",
            tytul="Test Event",
            opis="Test description",
        )

    def test_zdarzenie_creation(self):
        """Test that a ZdarzenieSpoleczne can be created."""
        self.assertEqual(self.zdarzenie.tytul, "Test Event")
        self.assertEqual(self.zdarzenie.kategoria2, "zgloszenie")

    def test_default_values(self):
        """Test default values are set correctly."""
        self.assertEqual(self.zdarzenie.like, 0)
        self.assertEqual(self.zdarzenie.dislike, 0)
        self.assertEqual(self.zdarzenie.min_wiek, 0)
        self.assertFalse(self.zdarzenie.dla_niepelnosprawnych)

    def test_str_method(self):
        """Test string representation."""
        self.assertIn("Test Event", str(self.zdarzenie))


class KomentarzModelTest(TestCase):
    """Tests for the Komentarz model."""

    def setUp(self):
        """Set up test data."""
        self.zdarzenie = ZdarzenieSpoleczne.objects.create(
            lokalizacja_lat=54.35,
            lokalizacja_lng=18.65,
            kategoria2="wydarzenie",
            tytul="Event for Comment",
            opis="Description",
        )
        self.komentarz = Komentarz.objects.create(
            zdarzenie=self.zdarzenie,
            autor="TestUser",
            tresc="This is a test comment",
        )

    def test_komentarz_creation(self):
        """Test that a Komentarz can be created."""
        self.assertEqual(self.komentarz.autor, "TestUser")
        self.assertEqual(self.komentarz.tresc, "This is a test comment")

    def test_komentarz_relation(self):
        """Test the relation to ZdarzenieSpoleczne."""
        self.assertEqual(self.komentarz.zdarzenie, self.zdarzenie)
        self.assertIn(self.komentarz, self.zdarzenie.komentarze.all())


class DzielnicaAPITest(APITestCase):
    """API tests for Dzielnica endpoints."""

    def setUp(self):
        """Set up test data."""
        self.dzielnica = Dzielnica.objects.create(
            dzielnica="API Test District",
            geometry={"type": "Polygon", "coordinates": []},
            powierzchnia=5.0,
        )

    def test_list_dzielnice(self):
        """Test listing all dzielnice."""
        response = self.client.get('/api/dzielnice/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dzielnice_geojson(self):
        """Test GeoJSON endpoint."""
        response = self.client.get('/api/dzielnice-geojson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "FeatureCollection")


class ZdarzeniaAPITest(APITestCase):
    """API tests for ZdarzenieSpoleczne endpoints."""

    def setUp(self):
        """Set up test data."""
        self.zdarzenie = ZdarzenieSpoleczne.objects.create(
            lokalizacja_lat=54.35,
            lokalizacja_lng=18.65,
            kategoria2="zgloszenie",
            tytul="API Test Event",
            opis="API test description",
        )

    def test_list_zdarzenia(self):
        """Test listing all zdarzenia."""
        response = self.client.get('/api/zdarzenia/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_zdarzenia_geojson(self):
        """Test GeoJSON endpoint for zdarzenia."""
        response = self.client.get('/api/zdarzenia-geojson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "FeatureCollection")

    def test_like_zdarzenie(self):
        """Test liking a zdarzenie."""
        initial_likes = self.zdarzenie.like
        response = self.client.post(f'/api/zdarzenia/{self.zdarzenie.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.zdarzenie.refresh_from_db()
        self.assertEqual(self.zdarzenie.like, initial_likes + 1)

    def test_dislike_zdarzenie(self):
        """Test disliking a zdarzenie."""
        initial_dislikes = self.zdarzenie.dislike
        response = self.client.post(f'/api/zdarzenia/{self.zdarzenie.id}/dislike/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.zdarzenie.refresh_from_db()
        self.assertEqual(self.zdarzenie.dislike, initial_dislikes + 1)


class AdminLoginAPITest(APITestCase):
    """API tests for admin login endpoint."""

    def test_login_with_correct_password(self):
        """Test login with correct password."""
        response = self.client.post('/api/admin-login/', {'password': 'admin123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertTrue(response.data['isAdmin'])

    def test_login_with_wrong_password(self):
        """Test login with incorrect password."""
        response = self.client.post('/api/admin-login/', {'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
