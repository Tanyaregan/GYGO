import unittest

from server import app
from model import db, connect_to_db, test_db


class GygoTests(unittest.TestCase):
    """Tests for main GYGO routes."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        connect_to_db(app, "postgresql:///characters")

    #####################################################################
    # flask Main route tests

    def test_index(self):
        result = self.client.get("/")
        self.assertIn('Or you just get a really cool outfit', result.data)

    def test_title_page(self):
        result = self.client.get("/titles")
        self.assertIn('All Titles', result.data)

    def test_house_page(self):
        result = self.client.get("/houses")
        self.assertIn('All Houses', result.data)

    def test_episodes_page(self):
        result = self.client.get("/episodes")
        self.assertIn('All Episodes', result.data)

    def test_chars_page(self):
        result = self.client.get("/chars")
        self.assertIn('All Characters', result.data)

    def test_search_one_result(self):
        result = self.client.get("/search")
        self.assertIn('Character name', result.data)

    def test_search_multi_result(self):
        result = self.client.get("/results", data={'char_male': False})
        self.assertIn('These characters', result.data)

    def test_search_single_result(self):
        result = self.client.get("/results", data={'char_name': 'Jon Snow'})
        self.assertIn('Jon Snow', result.data)

    ######################################################################
    # flask detail route tests

    def test_title_detail_page(self):
        result = self.client.get("/titles/92")
        self.assertIn('Breaker of Chains', result.data)

    def test_house_detail_page(self):
        result = self.client.get("/houses/216")
        self.assertIn('Iron Bank of Braavos', result.data)

    def test_episodes_detail_page(self):
        result = self.client.get("/episodes/13")
        self.assertIn('What Is Dead May Never Die', result.data)

    def test_char_detail_page(self):
        result = self.client.get("/chars/803")
        self.assertIn('Hot Pie', result.data)

    def test_item_detail_page(self):
        result = self.client.get("/chars/1206/item")
        self.assertIn('eBay Items', result.data)

#####################################################################
# db tests


class GygoTestsDatabase(unittest.TestCase):
    """Flask tests that use test database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        test_db()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_char(self):
        """Test char main page."""

        result = self.client.get("/chars")
        self.assertIn("char_1", result.data)

    def test_title(self):
        """Test title main page."""

        result = self.client.get("/titles")
        self.assertIn("title_2", result.data)

    def test_episodes(self):
        """Test mmain episode page."""

        result = self.client.get("/episodes")
        self.assertIn("episode_1", result.data)

    def test_house(self):
        """Test departments page."""

        result = self.client.get("/houses")
        self.assertIn('house_2_electric_boogaloo', result.data)




if __name__ == "__main__":
    unittest.main()