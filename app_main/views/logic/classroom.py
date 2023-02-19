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
                str(les["id"]): stud.marks.get(classroom_name, {}).get(
                    str(les["id"])
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
                    "id": les.get("id"),
                    "title": les.get("title"),
                    "date": date,
                    "dateform": les.get("date"),
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
    def post(  # noqa: CCR001
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponseRedirect:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))

        students: list = []
        student_users_raw = classroom.student.all()
        student_users = list(student_users_raw)

        for stud in student_users:
            prf = models.Profile.objects.get(user_id=stud.id)
            students.append(prf)

        if request.POST.get("newlesson"):
            newles_title = request.POST.get("newlesson_title")
            list_id = [les["id"] for les in classroom.lessons]
            newles_id = len(classroom.lessons)
            while newles_id in list_id:
                newles_id += 1
            classroom.lessons.append(
                {
                    "id": newles_id,
                    "title": newles_title,
                    "date": request.POST.get("newlesson_date"),
                }
            )
            classroom.save()

            for student in students:
                marks = student.marks
                try:
                    marks_current_class = marks[classroom.name]
                except KeyError:
                    student.marks[classroom.name] = {}
                    marks_current_class = marks.get(classroom.name)
                marks_current_class[newles_id] = request.POST.get(
                    f"{student.name}{student.lastname}_newlesson"
                )
                student.save()

        if request.POST.get("commitchanges"):
            for lesson in classroom.lessons:
                lid = lesson["id"]
                ltitle = lesson["title"]
                newltitle = request.POST.get(f"{ltitle}_title")
                lesson["title"] = newltitle
                lesson["date"] = request.POST.get(f"{ltitle}_date")
                for student in students:
                    marks = student.marks
                    marks_current_class = marks.get(classroom.name)
                    marks_current_class[lesson["id"]] = request.POST.get(
                        f"{student.name}{student.lastname}_lesson{lid}"
                    )
                    if ltitle != lesson["title"]:
                        del marks_current_class[ltitle]
                    student.save()
            classroom.save()

        return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")
