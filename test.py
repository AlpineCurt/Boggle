from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.board = [
                ['P', 'R', 'Z', 'R', 'C'],
                ['O', 'I', 'N', 'T', 'S'],
                ['Q', 'J', 'H', 'D', 'E'],
                ['O', 'R', 'S', 'Z', 'Q'],
                ['W', 'J', 'I', 'B', 'R']
            ]

    def tearDown(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session.clear()

    def test_home_new_page(self):
        """First visit to page, or a new game"""
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Boggle!</h1>", html)
            self.assertIn('game_board', list(session.keys()))

    def test_home_revisit(self):
        """Reloading page with game in progress"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = 'fake_test_board'

            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['game_board'], 'fake_test_board')
    
    def test_word_check(self):
        """JSON responses for word check"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = self.board
            
            # Valid word on board
            res1 = client.get("/word-check?word=ship")
            data1 = res1.get_data(as_text=True)
            self.assertIn("result", data1)
            self.assertIn("ok", data1)
            self.assertNotIn("not-a-word", data1)
            self.assertNotIn("not-on-board", data1)

            # Valid word, not on baord
            res2 = client.get("/word-check?word=right")
            data2 = res2.get_data(as_text=True)
            self.assertIn("result", data2)
            self.assertNotIn("ok", data2)
            self.assertNotIn("not-a-word", data2)
            self.assertIn("not-on-board", data2)

            # Invalid word
            res3 = client.get("/word-check?word=derp")
            data3 = res3.get_data(as_text=True)
            self.assertIn("result", data3)
            self.assertNotIn("ok", data3)
            self.assertIn("not-a-word", data3)
            self.assertNotIn("not-on-board", data3)

            # No word passed in query
            res4 = client.get("/word-check")
            data4 = res4.get_data(as_text=True)
            self.assertIn("result", data4)
            self.assertNotIn("ok", data4)
            self.assertNotIn("not-a-word", data4)
            self.assertNotIn("not-on-board", data4)