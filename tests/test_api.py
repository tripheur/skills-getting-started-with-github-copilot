from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 2,
                "participants": ["michael@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 2,
                "participants": ["emma@mergington.edu"],
            },
        }
    )


def test_signup_success_for_new_email_when_space_available():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_email():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_when_activity_is_full():
    # Arrange
    reset_activities()
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.post("/activities/Chess%20Club/signup?email=another@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "No spots left for Chess Club"


def test_unregister_participant_removes_email():
    # Arrange
    reset_activities()
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.delete("/activities/Chess%20Club/participants?email=daniel@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
