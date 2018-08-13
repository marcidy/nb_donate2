import os
import shutil
import tempfile

import pytest

import donate
from donate.database import db
from donate import models

from flask_migrate import (
    init,
    migrate,
    upgrade,
)


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    mig_path = tempfile.mkdtemp()
    os.rmdir(mig_path)

    app = donate.create_app({
        'TESTING': True,
        'DATABASE': db_path,
        })

    client = app.test_client()

    with app.app_context():
        db.create_all()
        # init(mig_path)
        # migrate(mig_path)
        # upgrade(mig_path)

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
    # shutil.rmtree(mig_path)


def test_user_creation(client):
    u = models.User(username="John", slack="jslack", email="john@email.net")
    db.session.add(u)
    users = models.User.query.all()
    assert len(users) == 1
