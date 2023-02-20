from typing import Any

roles = [
    (
        "student",
        "Student",
    ),
    (
        "teacher",
        "Teacher",
    ),
    (
        "director",
        "Director",
    ),
]

roles_priorities = {
    "student": 1,
    "teacher": 2,
    "director": 3,
}

marks: list = ["NA", 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def get_all_teachers_as_choices() -> Any:
    from django.contrib.auth import get_user_model

    user = get_user_model()
    teachers_queryset = user.objects.filter(
        profile__role="teacher"
    ) | user.objects.filter(profile__role="director")
    choices = [(obj.id, obj.username) for obj in teachers_queryset]
    return choices
