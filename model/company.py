from typing import Optional

from pydantic import BaseModel
from pydantic import Field
class Company(BaseModel):
    def __init__(self, id, name, categoryName):
        self.id = id
        self.name = name
        self.categoryName = categoryName
    id: int = Field(
        description="The unique id of this data model element",
        ge=0
    )
    name: str = Field(
        description="Company name",
    )
    categoryName: str = Field(
        description="Category name",
    )