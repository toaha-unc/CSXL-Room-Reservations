from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.group_user import GroupUser
from .entity_base import EntityBase
from typing import Self
from datetime import datetime

__authors__ = ["Kyle Chen"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class GroupUserEntity(EntityBase):
    """Serves as a database model for a user in a group"""

    __tablename__ = "group_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gid: Mapped[int] = mapped_column(ForeignKey("groups.gid"))
    pid: Mapped[int] = mapped_column(ForeignKey("user.pid"))
    groups: Mapped["GroupEntity"] = relationship(back_populates="participants")
    users: Mapped["UserEntity"] = relationship(back_populates="groups")

    @classmethod
    def from_model(cls, model: GroupUser) -> Self:
        """
        Class method that converts an `GroupUser` model into a `GroupUserEntity`

        Parameters:
            - model (GroupUser): Model to convert into an entity
        Returns:
            GroupUserEntity: Entity created from model
        """
        return cls(
            id=model.id,
            gid=model.gid,
            pid=model.pid,
        )

    def to_model(self) -> GroupUser:
        """
        Convert the GroupUserEntity ORM object to a GroupUser Pydantic model

        Returns:
            GroupUser: `GroupUser` object from the entity
        """
        return GroupUser(id=self.id, gid=self.gid, pid=self.pid)
