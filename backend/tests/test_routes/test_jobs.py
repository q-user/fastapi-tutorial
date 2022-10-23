import json
from typing import List

import pytest
from db.models.jobs import Job
from db.models.users import User
from db.repository.jobs import create_new_job
from db.repository.users import create_new_user
from schemas.jobs import JobCreate
from schemas.users import UserCreate


@pytest.fixture(scope="function")
def users(db_session) -> List[User]:
    users = []
    for i in range(5):
        username = f"user{i}"
        user_create = UserCreate(
            username=username, email=f"{username}@example.com", password="password"
        )
        users.append(create_new_user(user_create, db_session))
    return users


@pytest.fixture(scope="function")
def job_data(db_session) -> dict:
    return {
        "title": "SDE super",
        "company": "doodle",
        "company_url": "http://www.doodle.com",
        "location": "USA, NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }


@pytest.fixture(scope="function")
def jobs(users, job_data, db_session) -> List[Job]:
    jobs = []
    for i in range(1, 5):
        job_create = JobCreate(**job_data)
        jobs.append(create_new_job(job_create, db=db_session, owner_id=users[i].id))
    return jobs


def test_create_job(client, job_data, users):
    response = client.post("/jobs/", json.dumps(job_data))
    assert response.status_code == 200
    assert response.json()["company"] == "doodle"
    assert response.json()["description"] == "python"


def test_read_job(client, users, jobs):
    response = client.get("/jobs/1/")
    assert response.status_code == 200
    assert response.json()["title"] == "SDE super"


def test_read_all_jobs(client, users, jobs):
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_delete_job(client, jobs, db_session):
    job_id = jobs[0].id
    assert db_session.query(Job).filter(Job.id == job_id).first() is not None
    client.delete(f"/jobs/{jobs[0].id}")
    assert db_session.query(Job).filter(Job.id == job_id).first() is None
