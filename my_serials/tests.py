from django.test import TestCase, Client
import ddt
from my_serials import models


@ddt.ddt
class SerialTestCase(TestCase):

    def setUp(self):
        super(SerialTestCase, self).__init__()
        self.client = Client()
        self.user = models.User.objects.create(username='root')
        self.user.set_password('root')
        self.user.save()

    def test_serial_create(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/add/',
                                    {'serial_id': 60735},
                                    HTTP_REFERER='/home')
        serial = models.Serial.objects.get()
        self.assertEqual(serial.serial_id, 60735)
        self.assertEqual(serial.title, 'The Flash')
        self.assertEqual(serial.air_date, '2014')

    def test_serial_created_return_302(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/add/',
                                    {'serial_id': 60735},
                                    HTTP_REFERER='/home')
        self.assertEqual(response.status_code, 302)

    def test_serial_delete_return_301(self):
        self.client.login(username='root', password='root')
        serial = models.Serial(serial_id=60735,
                               title='test_title',
                               air_date='2014',
                               owner=self.user)
        serial.save()
        response = self.client.post('/delete/<int:serial.serial_id>',
                                    {},
                                    HTTP_REFERER='/home')
        self.assertEqual(response.status_code, 301)

    def test_detail_return_200(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/details/60735')
        self.assertEqual(response.status_code, 200)

    def test_popular_return_200(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/popular/')
        self.assertEqual(response.status_code, 200)

    def test_on_air_return_200(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/on-air-today/')
        self.assertEqual(response.status_code, 200)

    @ddt.data(
        (60735, 'The Flash'),
        (82856, 'The Mandalorian'),
        (79744, 'The Rookie'),
    )
    @ddt.unpack
    def test_right_title_created(self, serial_id, expected_title):
        self.client.login(username='root', password='root')
        response = self.client.post('/add/', {'serial_id': serial_id}, HTTP_REFERER='/home')
        serial = models.Serial.objects.get()
        self.assertEqual(serial.title, expected_title)
