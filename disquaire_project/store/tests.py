# TestCase  hérite de Unittest
from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Contact, Booking

# Index page
    # test that index page returns a 200
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

# Detail Page
class DetailPageTestCase(TestCase):
    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        album_imaginaire = Album.objects.create(title="existe pas")
        album_id = Album.objects.get(title='existe pas').id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the item does not exist
    def test_detail_page_returns_404(self):
        album_imaginaire = Album.objects.create(title="existe pas")
        album_id = (Album.objects.get(title='existe pas').id)+1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)

# Booking Page
class BookingPageTestCase(TestCase):
    #la fonction setUp est systématiquement lancée avant les tests unitaires.
    # C'est un excellent emplacement pour déclarer ses objets qu'on utilisera dans les tests
    def setUp(self):
        Contact.objects.create(name="Francois Pignon", email="francois.pignon@gogo.fr")
        album_imaginaire = Album.objects.create(title="existe pas")
        mikaelyoun = Artist.objects.create(name="mikael youn")
        album_imaginaire.artists.add(mikaelyoun)
        self.album = Album.objects.get(title='existe pas')
        self.contact = Contact.objects.get(name='Francois Pignon')

    # test that a new booking is made
    def test_new_booking_made(self):
        old_bookings = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name, 'email': email})
        new_booking= Booking.objects.count()
        self.assertEqual(new_booking, old_bookings+1)

    # test that a booking belongs to a contact
    def test_booking_belongs_contact(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.contact, booking.contact)

    # test that a booking belongs to an album
    def test_booking_belongs_album(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.album, booking.album)

    # test that an album is not available after a booking is made
    def test_album_not_available_anymore(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email
        })
        # Make the query again, otherwise `available` will still be set at `True`
        self.album.refresh_from_db()
        self.assertFalse(self.album.available)
