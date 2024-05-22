from pydantic import BaseModel
from . import User, Group

class GroupDetails(Group):
    """
    Pydantic model to represent a `Group`, including back-populated
    relationship fields.

    This model is based on the particpants section in `GroupEntity` model, which defines the shape
    of the `Group` database in the PostgreSQL database.
    """
    participants: list[User]