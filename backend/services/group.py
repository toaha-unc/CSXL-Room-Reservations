from fastapi import Depends, APIRouter, Depends, HTTPException
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import db_session
from ..models import User, UserDetails, Paginated, PaginationParams, Group, GroupDetails
from ..entities import UserEntity, GroupEntity, GroupUserEntity
from .permission import PermissionService
from random import randint as rand
from ..services import UserService
from .exceptions import UserNotFoundException

class GroupService:
    """GroupService is the access layer to managing groups for group seating and reservations."""

    _session: Session
    _permission: PermissionService
    _usersvc: UserService

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
        usersvc: UserService = Depends(),
    ):
        """Initializes a new GroupService.

        Args:
            session (Session): The database session to use
        """
        self._session = session
        self._permission = permission
        self._usersvc = usersvc

    def create(self, subject: User, user_pids: list[int]) -> Group | None:
        """Create a group with users specified by their PIDs.

        Args:
            user_pids: The list of user PIDs for the group.
            subject: A valid user

        Returns:
            The created Group model.

        Raises:
            Rollback if there is an error while creating a group.
        """
        # Make sure all users are valid before adding any to session

        if len(user_pids) < 2:
            raise Exception("Must have at least two users in a group")

        if len(user_pids) != len(set(user_pids)):
            raise Exception("Duplicate PIDs are not allowed in the group")

        # Validate that each PID is a 9-digit integer
        for pid in user_pids:
            if not isinstance(pid, int) or len(str(pid)) != 9:
                raise Exception(f"PID {pid} is not a valid 9-digit integer")

        for pid in user_pids:
            user = (
                self._session.query(UserEntity)
                .filter(UserEntity.pid == pid)
                .one_or_none()
            )
            if not user:
                raise UserNotFoundException(pid)

        entity = GroupEntity()
        self._session.add(entity)
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise

        for pid in user_pids:
            group_user = GroupUserEntity(gid=entity.gid, pid=pid)
            self._session.add(group_user)

        self._session.commit()

        return entity.to_model()

    def get_from_gid(self, subject: User, gid: int) -> list[User]:
        """Retrieve a group's user details for all users associated with the group.

        Args:
            gid: The unique identifier for the group whose user details are to be retrieved.
            subject: A valid user

        Returns:
            A list of `User` models with details for all users associated with the group identified by gid.

        Raises:
            Raises 404 exception if gid does not exist
        """

        # self._permission.enforce(subject, "group.create", f"group")

        try:
            user_pids = (
                self._session.query(GroupUserEntity.pid)
                .filter(GroupUserEntity.gid == gid)
                .all()
            )
            user_pids = [pid[0] for pid in user_pids]
            user: list[User] = []

            for pid in user_pids:
                valid_pid = (
                    self._session.query(UserEntity)
                    .filter(UserEntity.pid == pid)
                    .one_or_none()
                    .to_model()
                )
                if valid_pid:
                    user.append(valid_pid)
                else:
                    raise
            if len(user) == 0:
                raise Exception("No users found in this group")
            return user
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Group with ID {gid} not found or error: {str(e)}",
            )

    def get_group_from_pid(self, subject: User, pid: int) -> int:
        """Retrieve the group id of the user specified by the pid.

        Args:
            pid: The unique integer identifier for the user whose group ID is to be retrieved.
            subject: A valid user

        Returns:
            The group ID that the user is a member of.

        Raises:
            404 exception if pid is not associated with a group
        """
        # self._permission.enforce(subject, "group.create", f"group")

        try:
            group_id = (
                self._session.query(GroupUserEntity.gid)
                .filter(GroupUserEntity.pid == pid)
                .first()
            )
            return group_id[0]
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Error retrieving groups for PID {pid}: {str(e)}",
            )

    def delete(self, subject: User, gid: int) -> None:
        """Delete a group and its associated user-group relationships.

        Args:
            gid: The unique identifier of the group to be deleted.
            subject: A valid user

        Returns:
            None. The group and its associated data are removed from the database.

        Raises:
            Rollback exception if an error arrises while deleting a group.
        """
        # First, check if the group exists
        group_del = (
            self._session.query(GroupEntity)
            .filter(GroupEntity.gid == gid)
            .one_or_none()
        )
        if not group_del:
            raise UserNotFoundException(gid)

        # If group exists, proceed with deletion
        try:
            # Delete associated user-group relationships
            self._session.query(GroupUserEntity).filter(
                GroupUserEntity.gid == gid
            ).delete()

            # Delete the group
            self._session.delete(group_del)
            self._session.commit()

        except Exception as e:
            self._session.rollback()
            raise e

    def get_all_groups(self, subject: User) -> list[Group]:
        """Retrieve a list of all groups.

        Args:
            ssubject: A valid user

        Returns:
            A list of Group Objects that are in the system

        Raises:
            404 exception if there is an error while getting all groups
        """
        try:
            group_ids = self._session.query(GroupEntity).all()
            group_ids = [group.to_model() for group in group_ids]
            return group_ids
        except Exception as e:
            raise HTTPException(
                status_code=404,
            )
