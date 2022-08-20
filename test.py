from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        pass

    def tearDown(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session.clear()

    def test_home_new_page(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Boggle!</h1>", html)
            self.assertIn('game_board', list(session.keys()))

    def test_home_revisit(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = 'fake_test_board'

            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['game_board'], 'fake_test_board')