from pydantic import BaseModel, Field, ConfigDict


class PostsSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(max_length=50)
    content: str
    comments: str | None = None
    likes: int = Field(default=0)


