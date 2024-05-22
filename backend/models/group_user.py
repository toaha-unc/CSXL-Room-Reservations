from pydantic import BaseModel


class GroupUser(BaseModel):
    """
    Pydantic model to represent a `Group`, including back-populated
    relationship fields.

    This model is based on `GroupUserEntity` model, which defines the shape
    of the `Group` database in the PostgreSQL database.
    """
    id: int
    gid: int
    pid: int
