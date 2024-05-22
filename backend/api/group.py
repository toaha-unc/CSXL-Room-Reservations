"""User operations open to registered users such as searching for fellow user profiles."""

from fastapi import APIRouter, Depends, HTTPException
from ..services import UserService, GroupService
from ..models import User
from .authentication import registered_user
from ..models import Group, GroupDetails

api = APIRouter(prefix="/api/group")
openapi_tags = {
    "name": "Groups",
    "description": "Create a group",
}


@api.post("", response_model=Group, tags=["Groups"])
def create_group(
    user_pids: list[int],
    subject: User = Depends(registered_user),
    group_svc: GroupService = Depends(),
):
    """
    Create a new group of students

    Parameters:
        user_pids: a list of pids
        subject: a valid User model representing the currently logged in User
        group_svc: a valid GroupService

    Returns:
        Group: Created group

    Raises:
        HTTPException 400 if create() raises an Exception
    """
    try:
        return group_svc.create(subject, user_pids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/{gid}", response_model=list[User], tags=["Groups"])
def get_group(
    gid: int,
    subject: User = Depends(registered_user),
    group_svc: GroupService = Depends(),
):
    """
    Search for a group based on the organizers pid

    Parameters:
        gid: group id
        subject: a valid User model representing the currently logged in User
        group_svc: a valid GroupService

    Returns:
        list[User]: list of users in a group

    Raises:
        404 exception (from service)
    """
    return group_svc.get_from_gid(subject, gid)


@api.get("/user/{pid}", response_model=int, tags=["Groups"])
def get_user_group(
    pid: int,
    subject: User = Depends(registered_user),
    group_svc: GroupService = Depends(),
):
    """
    Returns a list of all group ids that a user is in

    Parameters:
        pid: users pid
        subject: a valid User model representing the currently logged in User
        group_svc: a valid GroupService

    Returns:
        int: group that a user is in

    Raises:
        404 exception (from service) if get_user_group raises exception
    """
    return group_svc.get_group_from_pid(subject, pid)


@api.delete("/{gid}", response_model=None, tags=["Groups"])
def delete_group(
    gid: int,
    subject: User = Depends(registered_user),
    group_svc: GroupService = Depends(),
):
    """
    Delete a group from the database

    Parameters:
        gid: group id
        subject: a valid User model representing the currently logged in User
        group_svc: a valid GroupService

    Returns:
        Database with group id and appropiate members deleted

    Raises:
        rollback exception (from service) if delete raises exception
    """
    return group_svc.delete(subject, gid)


@api.get("", response_model=list[Group], tags=["Groups"])
def get_all_groups(
    subject: User = Depends(registered_user), group_svc: GroupService = Depends()
):
    """
    Returns a list of all groups

    Parameters:
        subject: a valid User model representing the currently logged in User
        group_svc: a valid GroupService

    Returns:
        list[Group]: A list of all groups in the database

    Raises: 
        404 exception (from service) if get_all_groups raises exception
    """
    return group_svc.get_all_groups(subject)