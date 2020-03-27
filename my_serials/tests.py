from django.test import TestCase, Client
import ddt
from my_serials import models
from unittest import mock


@ddt.ddt
class SerialTestCase(TestCase):

    def setUp(self):
        super(SerialTestCase, self).__init__()
        self.client = Client()
        self.user = models.User(first_name='Eldar')
        self.user.save()

    def test_serial_created_return_302(self):
        response = self.client.post('/add/', {'serial_id': 60735})
        self.assertEqual(response.status_code, 302)

    def test_serial_create(self):
        serial = models.Serial(serial_id=60735,
                               title='test_title',
                               air_date='2014',
                               owner=self.user)
        serial.save()
        self.assertEqual(serial.serial_id, 60735)
        self.assertEqual(serial.title, 'test_title')
        self.assertEqual(serial.air_date, '2014')
        self.assertEqual(serial.owner, self.user)

    # @ddt.data(
    #     (60735, 'The Flash'),
    #     (82856, 'The Mandalorian'),
    #     (79744, 'The Rookie'),
    # )
    # @ddt.unpack
    # def test_right_title_created(self, serial_id, expected_title):
    #     response = self.client.post('/add/', {'serial_id': serial_id})
    #     serials = models.Serial.objects.all()
    #     for serial in serials:
    #         self.assertEqual(serial.title, expected_title)
