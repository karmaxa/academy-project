import datetime
from typing import Any

from django import http
from django import shortcuts
from django import views
from django.contrib.auth import get_user_model
from django.views import generic

from app_main import models
from app_main.views.logic import helpers

User = get_user_model()

marks: list = ["NA", 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


class ClassesView(generic.ListView):
    model = models.ClassRoom
    template_name = "app_main/classeslist.html"


class ClassRoomView(generic.DetailView):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponse:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))

        students = helpers.get_students_to_response(classroom)

        lessons, l_count = helpers.get_lessons_and_newlesid(classroom)

        response = shortcuts.render(
            self.request,
            "app_main/teacherclassroom.html",
            {
                "classroom": classroom,
                "students": students,
                "lessons": lessons,
                "marks": marks,
                "newles_title": "lesson" + str(l_count),
                "today": datetime.date.today().strftime("%Y-%m-%d"),
            },
        )
        return response


class ClassRoomEdit(views.View):
    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponseRedirect:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))

        if request.POST.get("newlesson"):
            helpers.add_new_lesson(request, classroom)

        if request.POST.get("commitchanges"):
            helpers.edit_classroom(request, classroom)

        return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")
