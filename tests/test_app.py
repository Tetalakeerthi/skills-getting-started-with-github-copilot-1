from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


client = TestClient(app)


def test_remove_participant_unregisters_the_student():
    response = client.post(
        f"/activities/Chess%20Club/signup?email={quote('student@example.com')}"
    )
    assert response.status_code == 200

    delete_response = client.delete(
        f"/activities/Chess%20Club/participants/{quote('student@example.com')}"
    )

    assert delete_response.status_code == 200
    assert "student@example.com" not in activities["Chess Club"]["participants"]


def test_remove_participant_returns_404_when_student_is_not_registered():
    response = client.delete(
        f"/activities/Chess%20Club/participants/{quote('missing@example.com')}"
    )

    assert response.status_code == 404
