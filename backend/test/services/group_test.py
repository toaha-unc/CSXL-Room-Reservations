"""Tests for the UserService class."""

# Tested Dependencies
from ...models.user import User, NewUser
from ...models.group import Group
from ...models.pagination import PaginationParams
from ...services import UserService, PermissionService, GroupService
from .fixtures import user_svc, user_svc_integration, permission_svc_mock, group_svc
from ...models.user import UserIdentity
from .core_data import user_data
import pytest
from fastapi import APIRouter, Depends, HTTPException


# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import user_svc, user_svc_integration, permission_svc_mock

# Data Models for Fake Data Inserted in Setup
from . import user_data
from .permission_data import (
    ambassador_permission,
    ambassador_permission_coworking_reservation,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_create(group_svc: GroupService, user_svc: UserService):
    """Test that a user can be retrieved by PID."""
    group = group_svc.create(
        user_data.root, [user_data.root.pid, user_data.ambassador.pid]
    )
    assert group is not None


def test_create_with_duplicates(group_svc: GroupService, user_svc: UserService):
    """Test creation of a group with duplicate PIDs should fail."""
    with pytest.raises(Exception) as exc_info:
        group_svc.create(user_data.root, [user_data.root.pid, user_data.root.pid])


def test_create_with_less_than_two_users(
    group_svc: GroupService, user_svc: UserService
):
    """Test creation of a group with less than two users should fail."""
    with pytest.raises(Exception) as exc_info:
        group_svc.create(user_data.root, [user_data.root.pid])


def test_invalid_create(group_svc: GroupService, user_svc: UserService):
    """Tests that we cannot create a group with an invalid pid"""
    with pytest.raises(Exception) as exc_info:
        group_svc.create(user_data.root, [user_data.root.pid, 123456789])
        pytest.fail("Expected Exception to be raised")


def test_invalid_create2(group_svc: GroupService, user_svc: UserService):
    """Tests that we are not able to create an empty group"""
    with pytest.raises(Exception) as exc_info:
        group_svc.create(user_data.root, [])
        pytest.fail("Expected Exception to be raised")


def test_big_create(group_svc: GroupService, user_svc: UserService):
    """Tests that we can create a group with many users"""
    group = group_svc.create(
        user_data.root,
        [
            user_data.root.pid,
            user_data.ambassador.pid,
            user_data.user.pid,
            user_data.dude.pid,
        ],
    )
    assert group is not None


def test_get(group_svc: GroupService, user_svc: UserService):
    """Tests that we can retrieve a group's members by its gid"""
    group = group_svc.create(
        user_data.root, [user_data.root.pid, user_data.ambassador.pid]
    )
    print(group.gid)
    users = group_svc.get_from_gid(user_data.ambassador, group.gid)
    assert len(users) == 2


def test_get_nonexistent_group(group_svc: GroupService, user_svc: UserService):
    """Tests that retrieving a nonexistent group should fail."""
    with pytest.raises(Exception) as exc_info:
        group = group_svc.get_from_gid(
            user_data.ambassador, 9999
        )  # Assuming this group doesn't exist


def test_retrieve_groups(group_svc: GroupService, user_svc: UserService):
    """Tests that we can retrieve all groups"""
    group_svc.create(user_data.root, [user_data.root.pid, user_data.ambassador.pid])
    group_svc.create(user_data.dude, [user_data.dude.pid, user_data.user.pid])
    groups = group_svc.get_all_groups(user_data.root)
    assert len(groups) == 3


def test_get_user_groups(group_svc: GroupService, user_svc: UserService):
    """Tests that we can retrieve the group that a user is in"""
    group = group_svc.create(
        user_data.root, [user_data.root.pid, user_data.ambassador.pid]
    )
    retrieved_gid = group_svc.get_group_from_pid(
        user_data.ambassador, user_data.ambassador.pid
    )
    assert group.gid == retrieved_gid


def test_get_user_groups_none(group_svc: GroupService, user_svc: UserService):
    """Tests that we expect to get an exception when a user is not in a group"""
    with pytest.raises(Exception):
        group_svc.get_group_from_pid(user_data.dude, user_data.dude.pid)


def test_delete_group(group_svc: GroupService, user_svc: UserService):
    """Tests that a user who isnt a part of any groups returns an empty list"""
    group1 = group_svc.create(
        user_data.root, [user_data.root.pid, user_data.ambassador.pid]
    )
    group2 = group_svc.create(user_data.dude, [user_data.dude.pid, user_data.user.pid])
    assert len(group_svc.get_all_groups(user_data.ambassador)) == 3
    group_svc.delete(user_data.root, group1.gid)
    assert len(group_svc.get_all_groups(user_data.ambassador)) == 2


def test_delete_nonexistant_group(group_svc: GroupService, user_svc: UserService):
    """Tests that we cannot attempt to delete a group that doesnt exist"""

    with pytest.raises(Exception) as exc_info:
        group_svc.delete(user_data.root, 9999)


def test_delete_twice(group_svc: GroupService, user_svc: UserService):
    """Tests that we cannot attempt to delete a group that doesnt exist"""
    group1 = group_svc.create(user_data.dude, [user_data.dude.pid, user_data.user.pid])
    group_svc.delete(user_data.root, group1.gid)
    with pytest.raises(Exception) as exc_info:
        group_svc.delete(user_data.root, group1.gid)
