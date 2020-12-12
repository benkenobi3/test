import pytest
from pytest_mock import mocker
from fastapi.testclient import TestClient
from .app.fastapi import app
from .mongo.models import Counter


def fake_get_region_id(region: str):
    regions = {'москва': 777}
    return regions.get(region)


def fake_add_counter(counter: Counter):
    pass


class TestAPI:
    def setup(self):
        self.client = TestClient(app)

    def teardown(self):
        pass

    def test_add_handler(self):
        invalid_data = {
            'phrase': '',
            'region': ''
        }
        response = self.client.post('/add', invalid_data)
        assert response.status_code == 400

        invalid_region_data = {
            'phrase': 'стиральные машинки',
            'region': 'abc'
        }
        response = self.client.post('/add', invalid_region_data)
        assert response.status_code == 404

        data = {
            'phrase': 'стиральные машинки',
            'region': 'москва'
        }
        response = self.client.post('/add', data)
        assert response.status_code == 201

    def test_stat_handler(self):
        pass
