from api import views
from api.models import Travel

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate


class TravelTestCase(TestCase):

    fixtures = [
        'api/fixtures/tests/user_1_with_3_travels.json',
        'api/fixtures/tests/user_2_without_travel.json',
        'api/fixtures/tests/user_3_with_1_travel.json',
    ]

    def setUp(self):

        self.user_with_3_travels = User.objects.get(id=1)
        self.user_without_travel = User.objects.get(id=2)
        self.user_with_1_travel = User.objects.get(id=3)
        self.TravelView = views.TravelView.as_view()
        self.factory = APIRequestFactory()

    def test_get_authenticated_travels(self):

        response = self._call_get_travels(self.user_with_3_travels)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], 3)

    def test_get_unauthenticated_travels(self):

        response = self._call_get_travels()
        self.assertEqual(response.status_code, 401)

    def test_get_user_travels_without_register(self):

        response = self._call_get_travels(self.user_without_travel)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_update_user_travel_only_evaluate_and_classification(self):

        travel_id = 1
        field_update = {
            'evaluate': 1,
            'classification': 2,
            'start_date': '1999-01-01T23:59:59Z',
            'finish_date': '1999-01-01T23:59:59Z',
        }

        current_travel = Travel.objects.get(id=travel_id)

        check_start_date = current_travel.start_date
        check_finish_date = current_travel.finish_date
        
        # assert before update
        self.assertEqual(current_travel.evaluate, None)
        self.assertEqual(current_travel.classification.id, 1)

        response = self._call_travel_update(travel_id, field_update)
        current_travel.refresh_from_db()

        # assert after update
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_travel.evaluate, 1)
        self.assertEqual(current_travel.classification.id, 2)
        self.assertEqual(current_travel.start_date, check_start_date)
        self.assertEqual(current_travel.finish_date, check_finish_date)

    def test_update_user_travel_evaluate(self):

        travel_id = 1
        field_update = {
            'evaluate': 1,
        }

        current_travel = Travel.objects.get(id=travel_id)
        
        # assert before update
        self.assertEqual(current_travel.evaluate, None)

        response = self._call_travel_update(travel_id, field_update)
        current_travel.refresh_from_db()

        # assert after update
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_travel.evaluate, 1)

    def test_update_user_travel_evaluate_with_less_than_one(self):

        travel_id = 1
        field_update = {
            'evaluate': 0,
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 400)

    def test_update_user_travel_evaluate_with_more_than_five(self):

        travel_id = 1
        field_update = {
            'evaluate': 6,
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 400)

    def test_update_user_travel_evaluate_with_float_value(self):

        travel_id = 1
        field_update = {
            'evaluate': 1.5,
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 400)

    def test_update_user_travel_evaluate_with_invalid_value(self):

        travel_id = 1
        field_update = {
            'evaluate': 'invalid_value',
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 400)

    def test_update_user_travel_classification(self):

        travel_id = 1
        field_update = {
            'classification': 2,
        }

        current_travel = Travel.objects.get(id=travel_id)
        
        # assert before update
        self.assertEqual(current_travel.classification.id, 1)

        response = self._call_travel_update(travel_id, field_update)
        current_travel.refresh_from_db()

        # assert after update
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_travel.classification.id, 2)

    def test_update_user_travel_with_invalid_classification(self):

        travel_id = 1
        field_update = {
            'classification': 0,
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 400)

    def test_update_user_travel_with_invalid_classification_value(self):

        travel_id = 1
        field_update = {
            'classification': 'invalid value',
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 400)

    def test_update_user_travel_with_nonexistent_travel_id(self):

        travel_id = 0
        field_update = {
            'classification': 2,
        }

        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 404)

    def test_update_user_travel_with_user_without_travel(self):

        travel_id = 0
        field_update = {
            'classification': 2,
        }

        request = self.factory.patch('/api/v1/travel/{}'.format(travel_id), field_update)
        force_authenticate(request, user=self.user_without_travel)
        response = self.TravelView(request, travel_id=travel_id)
        self.assertEqual(response.status_code, 404)

    def test_update_authenticated_travel(self):

        travel_id = 1
        field_update = {
            'classification': 2,
        }
        request = self.factory.patch('/api/v1/travel/{}'.format(travel_id), field_update)
        response = self.TravelView(request, travel_id=travel_id)
        self.assertEqual(response.status_code, 401)

    def test_update_travel_with_travel_id_from_another_user(self):

        travel_id = 4
        field_update = {
            'classification': 1,
        }
        response = self._call_travel_update(travel_id, field_update)
        self.assertEqual(response.status_code, 404)

    def test_create_travel(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 201)

    def test_create_travel_with_authenticated_user(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
        }
        response = self._call_post_travels(payload)
        self.assertEqual(response.status_code, 401)

    def test_create_travel_with_classification(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'classification': 1
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['classification'], 1)

    def test_create_travel_with_invalid_classification(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'classification': 0
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 400)

    def test_create_travel_with_evaluate(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'evaluate': 1
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['evaluate'], 1)

    def test_create_travel_with_evaluate_less_than_one(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'evaluate': 0
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 400)

    def test_create_travel_with_evaluate_more_than_five(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'evaluate': 6
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 400)

    def test_create_travel_with_classification_and_evaluate(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'classification': 1,
            'evaluate': 1
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['classification'], 1)
        self.assertEqual(response.data['evaluate'], 1)

    def test_create_travel_with_invalid_classification_and_evaluate(self):

        payload = {
            'start_date': '2020-01-01T00:00:00Z',
            'finish_date': '2020-02-01T00:00:00Z',
            'classification': 0,
            'classification': 0
        }
        response = self._call_post_travels(payload, self.user_without_travel)
        self.assertEqual(response.status_code, 400)

    def _call_travel_update(self, travel_id, field_update):

        request = self.factory.patch('/api/v1/travel/{}'.format(travel_id), field_update)
        force_authenticate(request, user=self.user_with_3_travels)
        return self.TravelView(request, travel_id=travel_id)

    def _call_get_travels(self, user=False):

        request = self.factory.get('/api/v1/travel')
        if user:
            force_authenticate(request, user=user)
        return self.TravelView(request)

    def _call_post_travels(self, payload, user=False):

        request = self.factory.post('/api/v1/travel', payload, 'json')
        if user:
            force_authenticate(request, user=user)
        return self.TravelView(request)
