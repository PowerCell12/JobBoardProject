import unittest

from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse


# Create your tests here.
class TestHomeView(TestCase):

    def setUp(self):
        self.test_client = Client()



    def test_home_view(self):

        response = self.test_client.get('/')

        self.assertTrue(response.status_code, 200)

        self.assertTemplateUsed(response, 'home.html')



# if __name__ == '__main__':
#     unittest.main()