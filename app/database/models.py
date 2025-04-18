from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class PostsModels(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    comments: Mapped[str | None] = None
    likes: Mapped[int | None] = None

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["UsersModel"] = relationship("UsersModel", back_populates="posts")


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True)
    about_me: Mapped[str | None]

    is_user: Mapped[bool] = mapped_column(default=True, server_default="True", nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default="False", nullable=False)

    posts: Mapped[list["PostsModels"]] = relationship("PostsModels", back_populates="users")
