from typing import Any

from django import http
from django import shortcuts
from django.contrib.auth import get_user_model
from django.views import generic

from app_main import models

User = get_user_model()

marks: list = ["NA", 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


class ClassRoomView(generic.DetailView):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponse:
        self.room = models.ClassRoom.objects.get(slug=kwargs.get("slug"))
        user_students = self.room.student.all()
        profile_students = [
            models.Profile.objects.get(user_id=stud.id)
            for stud in user_students
        ]
        classroom_name = self.room.name
        students = [
            {
                "name": stud.__str__(),
                "identifier": stud.name + stud.lastname,
                les["title"]: stud.marks.get(classroom_name, {}).get(
                    les["title"]
                ),
            }
            for stud in profile_students
            for les in self.room.lessons
        ]
        response = shortcuts.render(
            self.request,
            "app_main/teacherclassroom.html",
            {
                "classroom": self.room,
                "students": students,
                "lessons": self.room.lessons,
                "marks": marks,
            },
        )
        return response
