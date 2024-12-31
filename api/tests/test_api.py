import pytest
import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..app import config


'''class TestQueryVehicles():
    def test_query_makes(self, test_app: FastAPI, client: TestClient):
        """Ensure an assembled query for Makes returns both Toyota and Mazda."""
        response = client.get(f"/api/vehicles/makes",
            params = {})
        # Ensure this is a 200 response.
        assert response.status_code == 200
        # Get JSON response.
        response_json = response.json()
        # Ensure there's 2 in items.
        assert len(response_json["items"]) == 2

    def test_query_types(self, test_app: FastAPI, client: TestClient):
        """Ensure an assembled query for Types with make UID 'mazda-GANMfBBPNc' returns one type; Car."""
        response = client.get(f"/api/vehicles/types",
            params = {
                "mk": "mazda-GANMfBBPNc"})
        # Ensure this is a 200 response.
        assert response.status_code == 200
        # Get JSON response.
        response_json = response.json()
        # Ensure there's one type.
        assert len(response_json["items"]) == 1
        # Ensure that one type's name is 'Car'.
        response_json["items"][0]["name"] == "Car"

    def test_query_models(self, test_app: FastAPI, client: TestClient):
        """Ensure an assembled query for Models with make UID 'mazda-GANMfBBPNc' and type ID 'car' returns 3 models; '6', 'MX-5' and 'RX-7'"""
        response = client.get(f"/api/vehicles/models",
            params = {
                "mk": "mazda-GANMfBBPNc", 
                "t": "car"})
        # Ensure this is a 200 response.
        assert response.status_code == 200
        # Get JSON response.
        response_json = response.json()
        # Ensure there's three models.
        assert len(response_json["items"]) == 3

    def test_query_year_models(self, test_app: FastAPI, client: TestClient):
        """Ensure an assembled query for Models with make UID 'mazda-GANMfBBPNc', type ID 'car' and model UID 'rx-7-3exDTapq5g'"""
        response = client.get(f"/api/vehicles/years",
            params = {
                "mk": "mazda-GANMfBBPNc", 
                "t": "car", 
                "mdl": "rx-7-3exDTapq5g"})
        # Ensure this is a 200 response.
        assert response.status_code == 200
        # Get JSON response.
        response_json = response.json()
        # Ensure there are 10 results in total; because our page size is 10 items long. But really, there's 24 results in total.
        assert len(response_json["items"]) == 10
        # So check to ensure that 'total' is equal to 24
        assert response_json["total"] == 24

    def test_query_vehicles(self, test_app: FastAPI, client: TestClient):
        """Ensure an assembled query for Models with make UID 'mazda-GANMfBBPNc', type ID 'car', model UID 'rx-7-3exDTapq5g' and year 2000."""
        response = client.get(f"/api/vehicles/stock",
            params = {
                "mk": "mazda-GANMfBBPNc", 
                "t": "car", 
                "mdl": "rx-7-3exDTapq5g", 
                "y": "2000"})
        # Ensure this is a 200 response.
        assert response.status_code == 200
        # Get JSON response.
        response_json = response.json()
        # Ensure there's 4 in total.
        assert len(response_json["items"]) == 4


class TestPagination():
    def test_basic_pagination(self, test_app: FastAPI, client: TestClient):
        """Ensure we can query 3 pages for make UID 'mazda-GANMfBBPNc', type ID 'car' and model UID 'rx-7-3exDTapq5g'
        The first and second pages will contain 10 items, the third will contain 4 items."""
        expected_page_sizes = [10, 10, 4]
        for page, expected_size in zip(range(1, 4), expected_page_sizes):
            response = client.get(f"/api/vehicles/years",
                params = {
                    "mk": "mazda-GANMfBBPNc",
                    "t": "car", 
                    "mdl": 
                    "rx-7-3exDTapq5g", 
                    "page": page})
            # Ensure this is a 200 response.
            assert response.status_code == 200
            # Get JSON response.
            response_json = response.json()
            # Ensure there are expected size results in total.
            assert len(response_json["items"]) == expected_size'''