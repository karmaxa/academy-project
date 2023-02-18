import datetime
from typing import Any

from django import http
from django import shortcuts
from django import views
from django.contrib.auth import get_user_model
from django.views import generic

from app_main import models

User = get_user_model()

marks: list = ["NA", 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


class ClassesView(generic.ListView):
    model = models.ClassRoom
    template_name = "app_main/classeslist.html"


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
        students: list = []
        for stud in profile_students:
            mks = {
                les["title"]: stud.marks.get(classroom_name, {}).get(
                    les["title"]
                )
                for les in self.room.lessons
            }
            for lsn in mks:
                if mks[lsn] is None:
                    mks[lsn] = "null"
            students.append(
                {
                    "name": stud.__str__(),
                    "identifier": stud.name + stud.lastname,
                }
                | mks
            )
        lessons: list = []
        l_count: int = 1
        for les in self.room.lessons:
            l_count += 1
            date: str = ".".join(les.get("date").split("-")[::-1])
            lessons.append(
                {
                    "title": les.get("title"),
                    "date": date,
                }
            )
        response = shortcuts.render(
            self.request,
            "app_main/teacherclassroom.html",
            {
                "classroom": self.room,
                "students": students,
                "lessons": lessons,
                "marks": marks,
                "newles_title": "lesson" + str(l_count),
                "today": datetime.date.today().strftime("%Y-%m-%d"),
            },
        )
        return response


class ClassRoomAddLesson(views.View):
    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponseRedirect:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))
        classroom.lessons.append(
            {
                "title": request.POST.get("newlesson_title"),
                "date": request.POST.get("newlesson_date"),
            }
        )
        classroom.save()
        students: list = []

        student_users_raw = classroom.student.all()
        student_users = list(student_users_raw)
        for stud in student_users:
            prf = models.Profile.objects.get(user_id=stud.id)
            students.append(prf)

        for student in students:
            marks = student.marks
            marks_current_class = marks.get(classroom.name)
            marks_current_class[
                request.POST.get("newlesson_title")
            ] = request.POST.get(f"{student.name}{student.lastname}_newlesson")
            student.save()

        return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")
