import ddt
import tmdbsimple as tmdb
from django.test import TestCase, Client
from my_serials import models, views

tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


@ddt.ddt
class SerialTestCase(TestCase):

    def setUp(self):
        super(SerialTestCase, self).__init__()
        self.maxDiff = None
        self.client = Client()
        self.user = models.User.objects.create(username='root')
        self.user.set_password('root')
        self.user.save()

    def test_registration(self):
        response = self.client.post('/register/',
                                    data={'username': 'new_user',
                                          'email': 'test@example.com',
                                          'password': 'rootroot42',
                                          'password2': 'rootroot42'}
                                    )
        user = models.User.objects.get(username='new_user')
        self.assertEqual(response.context['new_user'], user)

    def test_edit_profile(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/profile/',
                                    data={'first_name': 'John',
                                          'second_name': 'Doe',
                                          'email': 'test2@example.com',
                                          'telegram_id': 123456789}
                                    )
        profile = models.Profile.objects.get(telegram_id=123456789)
        user = models.User.objects.get(profile=profile)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(profile.telegram_id, 123456789)

    def test_edit_profile_return_302(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/profile/',
                                    data={'first_name': 'John',
                                          'second_name': 'Doe',
                                          'email': 'test2@example.com',
                                          'telegram_id': 123456789}
                                    )
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        self.credentials = {'username': 'root',
                            'password': 'root'}
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_logout_return_200(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/logout/')
        self.assertEquals(response.status_code, 200)

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

    def test_localhost_redirect_302(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_serial_list_return_200(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_search_results(self):
        search_result = tmdb.Search().tv(query='Westworld')['results']
        self.client.login(username='root', password='root')
        response = self.client.get('/search/', {'query': 'Westworld'})
        self.assertNotEqual(response.context['search_result'], search_result)

    def test_search_no_results(self):
        search_result = tmdb.Search().tv(query='wasd')['results']
        self.client.login(username='root', password='root')
        response = self.client.get('/search/', {'query': 'wasd'})
        self.assertEqual(response.context['search_result'], search_result)

    def test_search_empty_results(self):
        search_result = []
        self.client.login(username='root', password='root')
        response = self.client.get('/search/', {'query': ''})
        self.assertEqual(response.context['search_result'], search_result)

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
        response = self.client.post('/add/',
                                    {'serial_id': serial_id},
                                    HTTP_REFERER='/home')
        serial = models.Serial.objects.get()
        self.assertEqual(serial.title, expected_title)

    @ddt.data(
        (60735, '2014'),
        (87049, 'N/A'),
        (79744, '2018'),
    )
    @ddt.unpack
    def test_right_air_date_created(self, serial_id, expected_date):
        self.client.login(username='root', password='root')
        response = self.client.post('/add/',
                                    {'serial_id': serial_id},
                                    HTTP_REFERER='/home')
        serial = models.Serial.objects.get()
        self.assertEqual(serial.air_date, expected_date)

    def test_serial_info(self):
        tv_info = views.serial_info(60735)
        self.assertEqual(tv_info['name'], 'The Flash')

    def test_user_serials(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/add/',
                                    {'serial_id': 60735},
                                    HTTP_REFERER='/home')
        serial_check_one = views.user_serials_check(self.user, 60735)
        serial_check_two = views.user_serials_check(self.user, 79744)
        self.assertEqual(serial_check_one, True)
        self.assertEqual(serial_check_two, False)
