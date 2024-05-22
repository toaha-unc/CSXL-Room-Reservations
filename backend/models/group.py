from pydantic import BaseModel


class Group(BaseModel):
    """
    Pydantic model to represent a `Group`, including back-populated
    relationship fields.

    This model is based on the gid section in `GroupEntity` model, which defines the shape
    of the `Group` database in the PostgreSQL database.
    """

    gid: int