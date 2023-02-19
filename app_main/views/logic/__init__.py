from .classroom import ClassesView
from .classroom import ClassRoomEdit
from .classroom import ClassRoomView
from .users import AllUsersView
from .users import UserDeleteView
from .users import UserDetailView
from .users import UserUpdateView

__all__ = [  # noqa: F405
    "AllUsersView",
    "UserDetailView",
    "UserDeleteView",
    "UserUpdateView",
    "ClassRoomView",
    "ClassesView",
    "ClassRoomEdit",
]
