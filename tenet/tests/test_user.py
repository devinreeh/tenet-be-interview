from django.test import Client, TestCase
from api.models import Users
import json
from uuid import uuid4
from http import HTTPStatus

class TestUsersEndpoint(TestCase):
    endpoint = '/api/users/%s/'


class TestGetUsersEndpoint(TestUsersEndpoint):

    def setUp(self):
        self.client = Client()
        self.test_user = Users.objects.create(name='John Doe')
    
    def test_successfully_get_user_with_id(self):
        user_id = str(self.test_user.id)
        response = self.client.get(self.endpoint%user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"id": user_id, "name": self.test_user.name})
    
    def test_successfully_return_404_for_missing_user(self):
        response = self.client.get(self.endpoint%str(uuid4()))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), {'error': 'User not found'})
        


class TestPostUsersEndpoint(TestUsersEndpoint):
    endpoint = '/api/users/'

    def setUp(self):
        self.test_user_name = "John Doe"

    def test_successfully_create_user(self):
        response = self.client.post(self.endpoint, data={"name": self.test_user_name}, content_type="application/json")
        user = Users.objects.get(name=self.test_user_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'success': 'User created %s'%(str(user.id))})
        self.assertEqual(user.name, self.test_user_name)
