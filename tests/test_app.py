from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    original_state = deepcopy(activities)
    yield
    # Cleanup
    activities.clear()
    activities.update(original_state)


client = TestClient(app)


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 400


def test_remove_participant_unregisters_the_student():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_remove_participant_returns_404_when_student_is_not_registered():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    # Assert
    assert response.status_code == 404
