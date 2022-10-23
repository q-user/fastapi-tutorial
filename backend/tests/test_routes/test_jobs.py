import json

import pytest

from db.models.users import User
from db.repository.users import create_new_user
from schemas.users import UserCreate


@pytest.fixture(scope="function")
def user(db_session) -> User:
    user_create = UserCreate(
        username="user", email="user@example.com", password="password"
    )
    return create_new_user(user_create, db_session)


def test_create_job(client, user):
    data = {
        "title": "SDE super",
        "company": "doodle",
        "company_url": "http://www.doodle.com",
        "location": "USA, NY",
        "description": "python",
        "date_posted": "2022-03-20"
    }
    response = client.post("/jobs/create-job/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["company"] == "doodle"
    assert response.json()["description"] == "python"


def test_read_job(client, user):
    data = {
        "title": "SDE super",
        "company": "doodle",
        "company_url": "www.doodle.com",
        "location": "USA, NY",
        "description": "python",
        "date_posted": "2022-03-20"
    }
    response = client.post("/jobs/create-job/", json.dumps(data))
    response = client.get("/jobs/get/1/")
    assert response.status_code == 200
    assert response.json()['title'] == "SDE super"
