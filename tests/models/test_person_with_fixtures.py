import json

import pytest
import werkzeug
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.datastructures import Authorization

from zou.app import app, db
from zou.app.models.person import Person
from zou.app.services import auth_service
from zou.app.utils.dbhelpers import get_db_uri

Base = declarative_base()

url = get_db_uri()
engine = create_engine(url)
Session = sessionmaker(bind=engine)


class ZouAuthorization(Authorization):
    def __init__(self, person: Person):
        super().__init__(auth_type="zou")
        self.person = person

    def to_header(self) -> str:
        access_token = create_access_token(
            identity=self.person.email,
            additional_claims={"user_id": self.person.id},
        )
        auth_service.register_tokens(app, access_token)
        return f"Bearer {access_token}"


class ZouFlaskClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_wrapper = werkzeug.test.TestResponse

    def authenticate(self, person):
        self.auth = ZouAuthorization(person)

    def open(self, *args, **kwargs):
        kwargs.setdefault("auth", self.auth)
        return super().open(*args, **kwargs)


@pytest.fixture()
def zou_app() -> app:
    app.testing = True
    app.test_client_class = ZouFlaskClient
    app.app_context().push()
    db.create_all()
    return app


@pytest.fixture()
def db_session():
    with Session() as session:
        yield session
        session.rollback()


@pytest.fixture()
def test_client(zou_app) -> ZouFlaskClient:
    return zou_app.test_client()


@pytest.fixture()
def superuser() -> Person:
    superuser = Person()
    superuser.first_name = "Super"
    superuser.last_name = "User"
    superuser.role = "admin"
    return superuser


@pytest.fixture()
def valid_person() -> Person:
    valid_person = Person()
    valid_person.first_name = "John"
    valid_person.last_name = "John"
    return valid_person


class TestPerson:
    def test_valid_person(self, db_session, valid_person):
        db_session.add(valid_person)

        person = db_session.query(Person).one()
        assert person.first_name == "John"

    def test_authenticated_person(self, db_session, test_client, superuser):
        test_client.authenticate(person=superuser)

        response = test_client.get("auth/authenticated")
        assert response.status_code == 200
        data = json.loads(response.data.decode("utf-8"))
        assert data["authenticated"]
