"""Mock data for users.

Three users are setup for testing and development purposes:

1. Rhonda Root (root user with all permissions)
2. Amy Ambassador (staff of XL with elevated permissions)
3. Sally Student (standard user without any special permissions)"""

import pytest
from sqlalchemy.orm import Session
from ....models.user import User
from ....entities import UserEntity, GroupUserEntity, GroupEntity
from ....entities.user_role_table import user_role_table
from ..reset_table_id_seq import reset_table_id_seq
from .. import role_data
from ....models import Group, GroupUser

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

groupUser1 = GroupUser(
    id=1,
    gid=1,
    pid=999999999,
)
groupUser2 = GroupUser(
    id=2,
    gid=1,
    pid=111111111,
)

group1 = Group(
    gid=1,
)


groupUsers = [groupUser1, groupUser2]
groups = [group1]


def insert_fake_data(session: Session):
    """Fake data to be inserted into the database to test groups."""
    global groups, groupUsers
    entities = []

    for group_user in groupUsers:
        entity = GroupUserEntity.from_model(group_user)
        session.add(entity)
        entities.append(entity)

    for group in groups:
        entity = GroupEntity.from_model(group)
        session.add(entity)
        entities.append(entity)

    reset_table_id_seq(session, GroupEntity, GroupEntity.gid, len(groups) + 1)
    reset_table_id_seq(
        session, GroupUserEntity, GroupUserEntity.id, len(groupUsers) + 1
    )
    session.commit()  # Commit to ensure User IDs in database

    # Associate Users with the Role(s) they are in


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
