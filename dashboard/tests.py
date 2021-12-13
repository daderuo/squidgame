from django.test import TestCase, Client

from .models import Game, User

# Create your tests here.

class UserTestCase(TestCase):

    def setUp(self):
        u = User.objects.create(username ='pippo', email = 'pippo@dadegame.com', password = '1234', total_games = 10, win_games = 5)
        u.set_password('1234')
        u.save()
        u = User.objects.create(username ='pluto', email = 'pluto@dadegame.com', password = '1234', total_games = 5, win_games = 10)
        u.set_password('1234')
        u.save()
        u = User.objects.create(username ='ciccio', email = 'ciccio@dadegame.com', password = '1234', total_games = -5, win_games = -10)
        u.set_password('1234')
        u.save()
        Game.objects.create(name = 'prova', img = 'photo/biglie_bg.jpeg')

    def test_valid_user(self):
        u1 = User.objects.get(username = 'pippo')
        self.assertTrue(u1.is_valid_user())

    def test_invalid_user(self):
        u2 = User.objects.get(username = 'pluto')
        self.assertFalse(u2.is_valid_user())

        u3 = User.objects.get(username = 'ciccio')
        self.assertFalse(u3.is_valid_user())

    def test_not_authenticated_users(self):
        c = Client()
        # response for non authenticated user
        response = c.get('')
        self.assertEqual(response.status_code,302)

        response = c.get('/game1/')
        self.assertEqual(response.status_code,302)

        response = c.get('',follow=True)
        self.assertEqual(response.status_code,200)

        response = c.get('/login/')
        self.assertEqual(response.status_code,200)

        response = c.get('/register/')
        self.assertEqual(response.status_code,200)

    def test_authentication_users(self):
        c = Client()
        #user authentication test
        self.assertEqual(c.login(username = 'pipp0',password = '1234'),False)

        self.assertEqual(c.login(username = 'pippo',password = '1234'),True)


    def test_authenticated_users(self):
        c = Client()
        self.assertEqual(c.login(username = 'pippo',password = '1234'),True)
        # response for authenticated user

        response = c.get('/game1/')
        self.assertEqual(response.status_code,200)

        response = c.get('')
        self.assertEqual(response.status_code,200)

        response = c.get('/logout/',follow=True)
        self.assertEqual(response.status_code,200)
