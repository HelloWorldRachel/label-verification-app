import io
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_partial_match_malt_and_hop(client):
    """
    Tests that a label with missing/mismatched fields (MALT & HOP) fails validation.
    """
    data = {
        'brand': 'MALT & HOP',
        'type': 'Ale with Honey and Huckleberry Flavor',
        'abv': '5%',
        'volume': '1 PINT, 0.9 FL. OZ.',
    }

    image_path = os.path.join(os.path.dirname(__file__), 'images', 'malt_and_hop.jpg')
    with open(image_path, 'rb') as img:
        data['label'] = (io.BytesIO(img.read()), 'malt_and_hop.jpg')
        response = client.post('/api/check-label', content_type='multipart/form-data', data=data)
        json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['success'] is False

    # Expect at least one field to fail
    mismatches = [field for field in json_data['details'] if not field['match']]
    assert len(mismatches) >= 1


def test_full_match_complete_label(client):
    """
    Tests that a complete label with correctly extracted fields passes validation.
    """
    data = {
        'brand': 'Fanciful Name Rose',
        'type': 'rose wine',
        'abv': '12.5%',
        'volume': '750 ml',
    }

    image_path = os.path.join(os.path.dirname(__file__), 'images', 'complete_label.jpg')
    with open(image_path, 'rb') as img:
        data['label'] = (io.BytesIO(img.read()), 'complete_label.jpg')
        response = client.post('/api/check-label', content_type='multipart/form-data', data=data)
        json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['success'] is True

    # All fields should match
    assert all(field['match'] for field in json_data['details'])