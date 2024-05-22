from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from .user_entity import UserEntity  # Import the UserEntity class
from ..models import User, Group, GroupDetails
from typing import Self

# from ..entities.group_user_table import group_user_table

# Assuming EntityBase, User, and group_user_table are already defined


class GroupEntity(EntityBase):
    """Serves as a database model for a group, which consists of that groups id and a list of participants"""

    __tablename__ = "groups"

    gid = mapped_column(Integer, primary_key=True, unique=True)
    participants: Mapped[list["GroupUserEntity"]] = relationship(
        back_populates="groups"
    )

    @classmethod
    def from_model(cls, model: Group) -> Self:
        """
        Class method that converts an `Group` model into a `GroupEntity`

        Parameters:
            - model (Group): Model to convert into an entity
        Returns:
            GroupEntity: Entity created from model
        """
        return cls(
            gid=model.gid,
        )

    def to_model(self) -> Group:
        """
        Convert the GroupEntity ORM object to a Group Pydantic model

        Returns:
            Group: `Group` object from the entity
        """
        return Group(
            gid=self.gid,
        )

    def to_details_model(self) -> GroupDetails:
        """
        Converts a `GroupEntity` object into a `GroupDetails` model object

        Returns:
            GroupDetails: `GroupDetails` object from the entity
        """
        return GroupDetails(
            gid=self.gid,
            # participants_pid=self.get_participant_pids(),
            participants=[user.to_model() for user in self.participants],
        )
